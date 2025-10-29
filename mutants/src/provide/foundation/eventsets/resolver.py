# provide/foundation/eventsets/resolver.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.eventsets.registry import get_registry
from provide.foundation.eventsets.types import EventMapping, FieldMapping

"""Event set resolution and enrichment logic."""
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


class EventSetResolver:
    """Resolves and applies event set enrichments to log events."""

    def xǁEventSetResolverǁ__init____mutmut_orig(self) -> None:
        """Initialize the resolver with cached configurations."""
        self._field_mappings: list[FieldMapping] = []
        self._event_mappings_by_set: dict[str, list[EventMapping]] = {}
        self._resolved = False

    def xǁEventSetResolverǁ__init____mutmut_1(self) -> None:
        """Initialize the resolver with cached configurations."""
        self._field_mappings: list[FieldMapping] = None
        self._event_mappings_by_set: dict[str, list[EventMapping]] = {}
        self._resolved = False

    def xǁEventSetResolverǁ__init____mutmut_2(self) -> None:
        """Initialize the resolver with cached configurations."""
        self._field_mappings: list[FieldMapping] = []
        self._event_mappings_by_set: dict[str, list[EventMapping]] = None
        self._resolved = False

    def xǁEventSetResolverǁ__init____mutmut_3(self) -> None:
        """Initialize the resolver with cached configurations."""
        self._field_mappings: list[FieldMapping] = []
        self._event_mappings_by_set: dict[str, list[EventMapping]] = {}
        self._resolved = None

    def xǁEventSetResolverǁ__init____mutmut_4(self) -> None:
        """Initialize the resolver with cached configurations."""
        self._field_mappings: list[FieldMapping] = []
        self._event_mappings_by_set: dict[str, list[EventMapping]] = {}
        self._resolved = True

    xǁEventSetResolverǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetResolverǁ__init____mutmut_1": xǁEventSetResolverǁ__init____mutmut_1,
        "xǁEventSetResolverǁ__init____mutmut_2": xǁEventSetResolverǁ__init____mutmut_2,
        "xǁEventSetResolverǁ__init____mutmut_3": xǁEventSetResolverǁ__init____mutmut_3,
        "xǁEventSetResolverǁ__init____mutmut_4": xǁEventSetResolverǁ__init____mutmut_4,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetResolverǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetResolverǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁEventSetResolverǁ__init____mutmut_orig)
    xǁEventSetResolverǁ__init____mutmut_orig.__name__ = "xǁEventSetResolverǁ__init__"

    def xǁEventSetResolverǁresolve__mutmut_orig(self) -> None:
        """Resolve all registered event sets into a unified configuration.

        This merges all registered event sets by priority, building
        the field mapping and event mapping lookup tables.
        """
        registry = get_registry()
        event_sets = registry.list_event_sets()  # Already sorted by priority

        # Clear existing state
        self._field_mappings.clear()
        self._event_mappings_by_set.clear()

        # Process each event set in priority order
        for event_set in event_sets:
            # Store event mappings by event set name
            self._event_mappings_by_set[event_set.name] = event_set.mappings

            # Add field mappings
            self._field_mappings.extend(event_set.field_mappings)

        self._resolved = True

    def xǁEventSetResolverǁresolve__mutmut_1(self) -> None:
        """Resolve all registered event sets into a unified configuration.

        This merges all registered event sets by priority, building
        the field mapping and event mapping lookup tables.
        """
        registry = None
        event_sets = registry.list_event_sets()  # Already sorted by priority

        # Clear existing state
        self._field_mappings.clear()
        self._event_mappings_by_set.clear()

        # Process each event set in priority order
        for event_set in event_sets:
            # Store event mappings by event set name
            self._event_mappings_by_set[event_set.name] = event_set.mappings

            # Add field mappings
            self._field_mappings.extend(event_set.field_mappings)

        self._resolved = True

    def xǁEventSetResolverǁresolve__mutmut_2(self) -> None:
        """Resolve all registered event sets into a unified configuration.

        This merges all registered event sets by priority, building
        the field mapping and event mapping lookup tables.
        """
        registry = get_registry()
        event_sets = None  # Already sorted by priority

        # Clear existing state
        self._field_mappings.clear()
        self._event_mappings_by_set.clear()

        # Process each event set in priority order
        for event_set in event_sets:
            # Store event mappings by event set name
            self._event_mappings_by_set[event_set.name] = event_set.mappings

            # Add field mappings
            self._field_mappings.extend(event_set.field_mappings)

        self._resolved = True

    def xǁEventSetResolverǁresolve__mutmut_3(self) -> None:
        """Resolve all registered event sets into a unified configuration.

        This merges all registered event sets by priority, building
        the field mapping and event mapping lookup tables.
        """
        registry = get_registry()
        event_sets = registry.list_event_sets()  # Already sorted by priority

        # Clear existing state
        self._field_mappings.clear()
        self._event_mappings_by_set.clear()

        # Process each event set in priority order
        for event_set in event_sets:
            # Store event mappings by event set name
            self._event_mappings_by_set[event_set.name] = None

            # Add field mappings
            self._field_mappings.extend(event_set.field_mappings)

        self._resolved = True

    def xǁEventSetResolverǁresolve__mutmut_4(self) -> None:
        """Resolve all registered event sets into a unified configuration.

        This merges all registered event sets by priority, building
        the field mapping and event mapping lookup tables.
        """
        registry = get_registry()
        event_sets = registry.list_event_sets()  # Already sorted by priority

        # Clear existing state
        self._field_mappings.clear()
        self._event_mappings_by_set.clear()

        # Process each event set in priority order
        for event_set in event_sets:
            # Store event mappings by event set name
            self._event_mappings_by_set[event_set.name] = event_set.mappings

            # Add field mappings
            self._field_mappings.extend(None)

        self._resolved = True

    def xǁEventSetResolverǁresolve__mutmut_5(self) -> None:
        """Resolve all registered event sets into a unified configuration.

        This merges all registered event sets by priority, building
        the field mapping and event mapping lookup tables.
        """
        registry = get_registry()
        event_sets = registry.list_event_sets()  # Already sorted by priority

        # Clear existing state
        self._field_mappings.clear()
        self._event_mappings_by_set.clear()

        # Process each event set in priority order
        for event_set in event_sets:
            # Store event mappings by event set name
            self._event_mappings_by_set[event_set.name] = event_set.mappings

            # Add field mappings
            self._field_mappings.extend(event_set.field_mappings)

        self._resolved = None

    def xǁEventSetResolverǁresolve__mutmut_6(self) -> None:
        """Resolve all registered event sets into a unified configuration.

        This merges all registered event sets by priority, building
        the field mapping and event mapping lookup tables.
        """
        registry = get_registry()
        event_sets = registry.list_event_sets()  # Already sorted by priority

        # Clear existing state
        self._field_mappings.clear()
        self._event_mappings_by_set.clear()

        # Process each event set in priority order
        for event_set in event_sets:
            # Store event mappings by event set name
            self._event_mappings_by_set[event_set.name] = event_set.mappings

            # Add field mappings
            self._field_mappings.extend(event_set.field_mappings)

        self._resolved = False

    xǁEventSetResolverǁresolve__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetResolverǁresolve__mutmut_1": xǁEventSetResolverǁresolve__mutmut_1,
        "xǁEventSetResolverǁresolve__mutmut_2": xǁEventSetResolverǁresolve__mutmut_2,
        "xǁEventSetResolverǁresolve__mutmut_3": xǁEventSetResolverǁresolve__mutmut_3,
        "xǁEventSetResolverǁresolve__mutmut_4": xǁEventSetResolverǁresolve__mutmut_4,
        "xǁEventSetResolverǁresolve__mutmut_5": xǁEventSetResolverǁresolve__mutmut_5,
        "xǁEventSetResolverǁresolve__mutmut_6": xǁEventSetResolverǁresolve__mutmut_6,
    }

    def resolve(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetResolverǁresolve__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetResolverǁresolve__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    resolve.__signature__ = _mutmut_signature(xǁEventSetResolverǁresolve__mutmut_orig)
    xǁEventSetResolverǁresolve__mutmut_orig.__name__ = "xǁEventSetResolverǁresolve"

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_orig(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_1(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = None
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_2(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(None, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_3(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, None)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_4(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_5(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(
            field_key,
        )
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_6(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_7(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = None

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_8(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).upper()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_9(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(None).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_10(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str not in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_11(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = None
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_12(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](None)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_13(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = None

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_14(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).upper()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_15(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(None).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_16(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = None

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_17(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            None,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_18(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            None,
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_19(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_20(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_21(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(None, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_22(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, None),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_23(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_24(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(
                event_mapping.default_key,
            ),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_25(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, "XXXX"),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_26(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str not in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_27(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key in event_dict:
                    event_dict[meta_key] = meta_value

        return visual_marker if visual_marker else None

    def xǁEventSetResolverǁ_process_field_enrichment__mutmut_28(
        self, field_key: str, field_value: Any, event_dict: dict[str, Any]
    ) -> str | None:
        """Process a single field for enrichment.

        Returns:
            Visual marker if found, None otherwise
        """
        event_mapping = self._find_event_mapping_for_field(field_key, field_value)
        if not event_mapping:
            return None

        value_str = str(field_value).lower()

        # Apply transformations
        if value_str in event_mapping.transformations:
            field_value = event_mapping.transformations[value_str](field_value)
            value_str = str(field_value).lower()

        # Get visual marker
        visual_marker = event_mapping.visual_markers.get(
            value_str,
            event_mapping.visual_markers.get(event_mapping.default_key, ""),
        )

        # Apply metadata fields
        if value_str in event_mapping.metadata_fields:
            for meta_key, meta_value in event_mapping.metadata_fields[value_str].items():
                if meta_key not in event_dict:
                    event_dict[meta_key] = None

        return visual_marker if visual_marker else None

    xǁEventSetResolverǁ_process_field_enrichment__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_1": xǁEventSetResolverǁ_process_field_enrichment__mutmut_1,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_2": xǁEventSetResolverǁ_process_field_enrichment__mutmut_2,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_3": xǁEventSetResolverǁ_process_field_enrichment__mutmut_3,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_4": xǁEventSetResolverǁ_process_field_enrichment__mutmut_4,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_5": xǁEventSetResolverǁ_process_field_enrichment__mutmut_5,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_6": xǁEventSetResolverǁ_process_field_enrichment__mutmut_6,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_7": xǁEventSetResolverǁ_process_field_enrichment__mutmut_7,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_8": xǁEventSetResolverǁ_process_field_enrichment__mutmut_8,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_9": xǁEventSetResolverǁ_process_field_enrichment__mutmut_9,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_10": xǁEventSetResolverǁ_process_field_enrichment__mutmut_10,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_11": xǁEventSetResolverǁ_process_field_enrichment__mutmut_11,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_12": xǁEventSetResolverǁ_process_field_enrichment__mutmut_12,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_13": xǁEventSetResolverǁ_process_field_enrichment__mutmut_13,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_14": xǁEventSetResolverǁ_process_field_enrichment__mutmut_14,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_15": xǁEventSetResolverǁ_process_field_enrichment__mutmut_15,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_16": xǁEventSetResolverǁ_process_field_enrichment__mutmut_16,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_17": xǁEventSetResolverǁ_process_field_enrichment__mutmut_17,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_18": xǁEventSetResolverǁ_process_field_enrichment__mutmut_18,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_19": xǁEventSetResolverǁ_process_field_enrichment__mutmut_19,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_20": xǁEventSetResolverǁ_process_field_enrichment__mutmut_20,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_21": xǁEventSetResolverǁ_process_field_enrichment__mutmut_21,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_22": xǁEventSetResolverǁ_process_field_enrichment__mutmut_22,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_23": xǁEventSetResolverǁ_process_field_enrichment__mutmut_23,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_24": xǁEventSetResolverǁ_process_field_enrichment__mutmut_24,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_25": xǁEventSetResolverǁ_process_field_enrichment__mutmut_25,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_26": xǁEventSetResolverǁ_process_field_enrichment__mutmut_26,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_27": xǁEventSetResolverǁ_process_field_enrichment__mutmut_27,
        "xǁEventSetResolverǁ_process_field_enrichment__mutmut_28": xǁEventSetResolverǁ_process_field_enrichment__mutmut_28,
    }

    def _process_field_enrichment(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetResolverǁ_process_field_enrichment__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetResolverǁ_process_field_enrichment__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _process_field_enrichment.__signature__ = _mutmut_signature(
        xǁEventSetResolverǁ_process_field_enrichment__mutmut_orig
    )
    xǁEventSetResolverǁ_process_field_enrichment__mutmut_orig.__name__ = (
        "xǁEventSetResolverǁ_process_field_enrichment"
    )

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_orig(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_1(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_2(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = None
        event_msg = event_dict.get("event", "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_3(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(None)
        event_msg = event_dict.get("event", "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_4(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "XXXX".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_5(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = None
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_6(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get(None, "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_7(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", None)
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_8(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_9(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get(
            "event",
        )
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_10(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("XXeventXX", "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_11(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("EVENT", "")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_12(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", "XXXX")
        event_dict["event"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_13(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", "")
        event_dict["event"] = None

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_14(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", "")
        event_dict["XXeventXX"] = f"{prefix} {event_msg}" if event_msg else prefix

    def xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_15(
        self, enrichments: list[str], event_dict: dict[str, Any]
    ) -> None:
        """Apply visual enrichments to the event message."""
        if not enrichments:
            return

        prefix = "".join(f"[{e}]" for e in enrichments)
        event_msg = event_dict.get("event", "")
        event_dict["EVENT"] = f"{prefix} {event_msg}" if event_msg else prefix

    xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_1": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_1,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_2": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_2,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_3": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_3,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_4": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_4,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_5": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_5,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_6": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_6,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_7": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_7,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_8": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_8,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_9": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_9,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_10": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_10,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_11": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_11,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_12": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_12,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_13": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_13,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_14": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_14,
        "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_15": xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_15,
    }

    def _apply_visual_enrichments(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _apply_visual_enrichments.__signature__ = _mutmut_signature(
        xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_orig
    )
    xǁEventSetResolverǁ_apply_visual_enrichments__mutmut_orig.__name__ = (
        "xǁEventSetResolverǁ_apply_visual_enrichments"
    )

    def xǁEventSetResolverǁenrich_event__mutmut_orig(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_1(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_2(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = None

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_3(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(None):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_4(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" and field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_5(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key != "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_6(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "XXeventXX" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_7(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "EVENT" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_8(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is not None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_9(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                break

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_10(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = None
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_11(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(None, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_12(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, None, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_13(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, None)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_14(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_15(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_16(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(
                field_key,
                field_value,
            )
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_17(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(None)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_18(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(None, event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_19(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(enrichments, None)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_20(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(event_dict)

        return event_dict

    def xǁEventSetResolverǁenrich_event__mutmut_21(self, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich a log event with event set data.

        Args:
            event_dict: The event dictionary to enrich

        Returns:
            The enriched event dictionary

        """
        if not self._resolved:
            self.resolve()

        enrichments = []

        # Process each field in the event
        for field_key, field_value in list(event_dict.items()):
            if field_key == "event" or field_value is None:
                continue

            visual_marker = self._process_field_enrichment(field_key, field_value, event_dict)
            if visual_marker:
                enrichments.append(visual_marker)

        # Add visual enrichments to event message
        self._apply_visual_enrichments(
            enrichments,
        )

        return event_dict

    xǁEventSetResolverǁenrich_event__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetResolverǁenrich_event__mutmut_1": xǁEventSetResolverǁenrich_event__mutmut_1,
        "xǁEventSetResolverǁenrich_event__mutmut_2": xǁEventSetResolverǁenrich_event__mutmut_2,
        "xǁEventSetResolverǁenrich_event__mutmut_3": xǁEventSetResolverǁenrich_event__mutmut_3,
        "xǁEventSetResolverǁenrich_event__mutmut_4": xǁEventSetResolverǁenrich_event__mutmut_4,
        "xǁEventSetResolverǁenrich_event__mutmut_5": xǁEventSetResolverǁenrich_event__mutmut_5,
        "xǁEventSetResolverǁenrich_event__mutmut_6": xǁEventSetResolverǁenrich_event__mutmut_6,
        "xǁEventSetResolverǁenrich_event__mutmut_7": xǁEventSetResolverǁenrich_event__mutmut_7,
        "xǁEventSetResolverǁenrich_event__mutmut_8": xǁEventSetResolverǁenrich_event__mutmut_8,
        "xǁEventSetResolverǁenrich_event__mutmut_9": xǁEventSetResolverǁenrich_event__mutmut_9,
        "xǁEventSetResolverǁenrich_event__mutmut_10": xǁEventSetResolverǁenrich_event__mutmut_10,
        "xǁEventSetResolverǁenrich_event__mutmut_11": xǁEventSetResolverǁenrich_event__mutmut_11,
        "xǁEventSetResolverǁenrich_event__mutmut_12": xǁEventSetResolverǁenrich_event__mutmut_12,
        "xǁEventSetResolverǁenrich_event__mutmut_13": xǁEventSetResolverǁenrich_event__mutmut_13,
        "xǁEventSetResolverǁenrich_event__mutmut_14": xǁEventSetResolverǁenrich_event__mutmut_14,
        "xǁEventSetResolverǁenrich_event__mutmut_15": xǁEventSetResolverǁenrich_event__mutmut_15,
        "xǁEventSetResolverǁenrich_event__mutmut_16": xǁEventSetResolverǁenrich_event__mutmut_16,
        "xǁEventSetResolverǁenrich_event__mutmut_17": xǁEventSetResolverǁenrich_event__mutmut_17,
        "xǁEventSetResolverǁenrich_event__mutmut_18": xǁEventSetResolverǁenrich_event__mutmut_18,
        "xǁEventSetResolverǁenrich_event__mutmut_19": xǁEventSetResolverǁenrich_event__mutmut_19,
        "xǁEventSetResolverǁenrich_event__mutmut_20": xǁEventSetResolverǁenrich_event__mutmut_20,
        "xǁEventSetResolverǁenrich_event__mutmut_21": xǁEventSetResolverǁenrich_event__mutmut_21,
    }

    def enrich_event(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetResolverǁenrich_event__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetResolverǁenrich_event__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    enrich_event.__signature__ = _mutmut_signature(xǁEventSetResolverǁenrich_event__mutmut_orig)
    xǁEventSetResolverǁenrich_event__mutmut_orig.__name__ = "xǁEventSetResolverǁenrich_event"

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_orig(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_1(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = None  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_2(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(None)[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_3(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split("XX.XX")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_4(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[+1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_5(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-2]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_6(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key and mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_7(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name != simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_8(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name != field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_9(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    or field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_10(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    or mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_11(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith(None)
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_12(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("XXhttp.XX")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_13(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("HTTP.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_14(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith(None)
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_15(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("XXhttp_XX")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_16(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("HTTP_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_17(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(None, "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_18(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", None) == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_19(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace("_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_20(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(
                        ".",
                    )
                    == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_21(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace("XX.XX", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_22(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "XX_XX") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_23(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") != mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_24(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    or field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_25(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    or mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_26(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith(None)
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_27(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("XXllm.XX")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_28(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("LLM.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_29(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith(None)
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_30(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("XXllm_XX")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_31(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("LLM_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_32(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(None, "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_33(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", None) == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_34(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace("_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_35(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(
                        ".",
                    )
                    == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_36(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace("XX.XX", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_37(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "XX_XX") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_38(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") != mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_39(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    or field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_40(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    or mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_41(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith(None)
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_42(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("XXdb.XX")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_43(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("DB.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_44(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith(None)
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_45(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("XXdb_XX")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_46(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("DB_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_47(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(None, "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_48(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", None) == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_49(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace("_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_50(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(
                        ".",
                    )
                    == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_51(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace("XX.XX", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_52(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "XX_XX") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_53(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") != mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_54(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    or field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_55(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    or mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_56(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith(None)
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_57(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("XXtask.XX")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_58(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("TASK.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_59(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith(None)
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_60(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("XXtask_XX")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_61(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("TASK_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_62(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(None, "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_63(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", None) == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_64(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace("_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_65(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(
                        ".",
                    )
                    == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_66(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace("XX.XX", "_") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_67(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "XX_XX") == mapping.name
                ):
                    return mapping

        return None

    def xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_68(
        self, field_key: str, field_value: Any
    ) -> EventMapping | None:
        """Find the appropriate EventMapping for a given field.

        This method uses a heuristic approach to match field keys to EventMappings:
        1. Direct field name mapping (e.g., "domain" -> "domain" mapping)
        2. Field prefix mapping (e.g., "http.method" -> "http_method" mapping)
        3. Field pattern matching
        """
        # First check for direct field name matches
        simple_key = field_key.split(".")[-1]  # Get last part of dotted key

        for _event_set_name, mappings in self._event_mappings_by_set.items():
            for mapping in mappings:
                # Direct name match
                if mapping.name == simple_key or mapping.name == field_key:
                    return mapping

                # Pattern matching for common cases
                if (
                    field_key.startswith("http.")
                    and mapping.name.startswith("http_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("llm.")
                    and mapping.name.startswith("llm_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("db.")
                    and mapping.name.startswith("db_")
                    and field_key.replace(".", "_") == mapping.name
                ):
                    return mapping

                if (
                    field_key.startswith("task.")
                    and mapping.name.startswith("task_")
                    and field_key.replace(".", "_") != mapping.name
                ):
                    return mapping

        return None

    xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_1": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_1,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_2": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_2,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_3": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_3,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_4": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_4,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_5": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_5,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_6": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_6,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_7": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_7,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_8": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_8,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_9": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_9,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_10": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_10,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_11": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_11,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_12": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_12,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_13": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_13,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_14": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_14,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_15": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_15,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_16": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_16,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_17": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_17,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_18": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_18,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_19": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_19,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_20": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_20,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_21": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_21,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_22": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_22,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_23": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_23,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_24": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_24,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_25": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_25,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_26": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_26,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_27": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_27,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_28": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_28,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_29": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_29,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_30": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_30,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_31": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_31,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_32": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_32,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_33": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_33,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_34": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_34,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_35": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_35,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_36": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_36,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_37": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_37,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_38": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_38,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_39": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_39,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_40": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_40,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_41": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_41,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_42": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_42,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_43": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_43,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_44": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_44,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_45": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_45,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_46": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_46,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_47": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_47,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_48": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_48,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_49": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_49,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_50": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_50,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_51": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_51,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_52": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_52,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_53": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_53,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_54": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_54,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_55": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_55,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_56": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_56,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_57": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_57,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_58": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_58,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_59": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_59,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_60": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_60,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_61": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_61,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_62": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_62,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_63": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_63,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_64": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_64,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_65": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_65,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_66": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_66,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_67": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_67,
        "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_68": xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_68,
    }

    def _find_event_mapping_for_field(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _find_event_mapping_for_field.__signature__ = _mutmut_signature(
        xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_orig
    )
    xǁEventSetResolverǁ_find_event_mapping_for_field__mutmut_orig.__name__ = (
        "xǁEventSetResolverǁ_find_event_mapping_for_field"
    )

    def xǁEventSetResolverǁget_visual_markers__mutmut_orig(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_1(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_2(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = None

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_3(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" and field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_4(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key != "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_5(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "XXeventXX" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_6(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "EVENT" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_7(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is not None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_8(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                break

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_9(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = None
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_10(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(None, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_11(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, None)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_12(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_13(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(
                field_key,
            )
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_14(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_15(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                break

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_16(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = None
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_17(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).upper()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_18(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(None).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_19(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = None

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_20(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                None,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_21(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                None,
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_22(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_23(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_24(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(None, ""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_25(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, None),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_26(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(""),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_27(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(
                    event_mapping.default_key,
                ),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_28(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, "XXXX"),
            )

            if marker:
                markers.append(marker)

        return markers

    def xǁEventSetResolverǁget_visual_markers__mutmut_29(self, event_dict: dict[str, Any]) -> list[str]:
        """Extract visual markers for an event without modifying it.

        Args:
            event_dict: The event dictionary to analyze

        Returns:
            List of visual markers that would be applied

        """
        if not self._resolved:
            self.resolve()

        markers = []

        for field_key, field_value in event_dict.items():
            if field_key == "event" or field_value is None:
                continue

            event_mapping = self._find_event_mapping_for_field(field_key, field_value)
            if not event_mapping:
                continue

            value_str = str(field_value).lower()
            marker = event_mapping.visual_markers.get(
                value_str,
                event_mapping.visual_markers.get(event_mapping.default_key, ""),
            )

            if marker:
                markers.append(None)

        return markers

    xǁEventSetResolverǁget_visual_markers__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁEventSetResolverǁget_visual_markers__mutmut_1": xǁEventSetResolverǁget_visual_markers__mutmut_1,
        "xǁEventSetResolverǁget_visual_markers__mutmut_2": xǁEventSetResolverǁget_visual_markers__mutmut_2,
        "xǁEventSetResolverǁget_visual_markers__mutmut_3": xǁEventSetResolverǁget_visual_markers__mutmut_3,
        "xǁEventSetResolverǁget_visual_markers__mutmut_4": xǁEventSetResolverǁget_visual_markers__mutmut_4,
        "xǁEventSetResolverǁget_visual_markers__mutmut_5": xǁEventSetResolverǁget_visual_markers__mutmut_5,
        "xǁEventSetResolverǁget_visual_markers__mutmut_6": xǁEventSetResolverǁget_visual_markers__mutmut_6,
        "xǁEventSetResolverǁget_visual_markers__mutmut_7": xǁEventSetResolverǁget_visual_markers__mutmut_7,
        "xǁEventSetResolverǁget_visual_markers__mutmut_8": xǁEventSetResolverǁget_visual_markers__mutmut_8,
        "xǁEventSetResolverǁget_visual_markers__mutmut_9": xǁEventSetResolverǁget_visual_markers__mutmut_9,
        "xǁEventSetResolverǁget_visual_markers__mutmut_10": xǁEventSetResolverǁget_visual_markers__mutmut_10,
        "xǁEventSetResolverǁget_visual_markers__mutmut_11": xǁEventSetResolverǁget_visual_markers__mutmut_11,
        "xǁEventSetResolverǁget_visual_markers__mutmut_12": xǁEventSetResolverǁget_visual_markers__mutmut_12,
        "xǁEventSetResolverǁget_visual_markers__mutmut_13": xǁEventSetResolverǁget_visual_markers__mutmut_13,
        "xǁEventSetResolverǁget_visual_markers__mutmut_14": xǁEventSetResolverǁget_visual_markers__mutmut_14,
        "xǁEventSetResolverǁget_visual_markers__mutmut_15": xǁEventSetResolverǁget_visual_markers__mutmut_15,
        "xǁEventSetResolverǁget_visual_markers__mutmut_16": xǁEventSetResolverǁget_visual_markers__mutmut_16,
        "xǁEventSetResolverǁget_visual_markers__mutmut_17": xǁEventSetResolverǁget_visual_markers__mutmut_17,
        "xǁEventSetResolverǁget_visual_markers__mutmut_18": xǁEventSetResolverǁget_visual_markers__mutmut_18,
        "xǁEventSetResolverǁget_visual_markers__mutmut_19": xǁEventSetResolverǁget_visual_markers__mutmut_19,
        "xǁEventSetResolverǁget_visual_markers__mutmut_20": xǁEventSetResolverǁget_visual_markers__mutmut_20,
        "xǁEventSetResolverǁget_visual_markers__mutmut_21": xǁEventSetResolverǁget_visual_markers__mutmut_21,
        "xǁEventSetResolverǁget_visual_markers__mutmut_22": xǁEventSetResolverǁget_visual_markers__mutmut_22,
        "xǁEventSetResolverǁget_visual_markers__mutmut_23": xǁEventSetResolverǁget_visual_markers__mutmut_23,
        "xǁEventSetResolverǁget_visual_markers__mutmut_24": xǁEventSetResolverǁget_visual_markers__mutmut_24,
        "xǁEventSetResolverǁget_visual_markers__mutmut_25": xǁEventSetResolverǁget_visual_markers__mutmut_25,
        "xǁEventSetResolverǁget_visual_markers__mutmut_26": xǁEventSetResolverǁget_visual_markers__mutmut_26,
        "xǁEventSetResolverǁget_visual_markers__mutmut_27": xǁEventSetResolverǁget_visual_markers__mutmut_27,
        "xǁEventSetResolverǁget_visual_markers__mutmut_28": xǁEventSetResolverǁget_visual_markers__mutmut_28,
        "xǁEventSetResolverǁget_visual_markers__mutmut_29": xǁEventSetResolverǁget_visual_markers__mutmut_29,
    }

    def get_visual_markers(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁEventSetResolverǁget_visual_markers__mutmut_orig"),
            object.__getattribute__(self, "xǁEventSetResolverǁget_visual_markers__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_visual_markers.__signature__ = _mutmut_signature(xǁEventSetResolverǁget_visual_markers__mutmut_orig)
    xǁEventSetResolverǁget_visual_markers__mutmut_orig.__name__ = "xǁEventSetResolverǁget_visual_markers"


# Global resolver instance
_resolver = EventSetResolver()


def get_resolver() -> EventSetResolver:
    """Get the global event set resolver instance."""
    return _resolver


def x_enrich_event__mutmut_orig(event_dict: dict[str, Any]) -> dict[str, Any]:
    """Enrich a log event with event set data.

    Args:
        event_dict: The event dictionary to enrich

    Returns:
        The enriched event dictionary

    """
    return _resolver.enrich_event(event_dict)


def x_enrich_event__mutmut_1(event_dict: dict[str, Any]) -> dict[str, Any]:
    """Enrich a log event with event set data.

    Args:
        event_dict: The event dictionary to enrich

    Returns:
        The enriched event dictionary

    """
    return _resolver.enrich_event(None)


x_enrich_event__mutmut_mutants: ClassVar[MutantDict] = {"x_enrich_event__mutmut_1": x_enrich_event__mutmut_1}


def enrich_event(*args, **kwargs):
    result = _mutmut_trampoline(x_enrich_event__mutmut_orig, x_enrich_event__mutmut_mutants, args, kwargs)
    return result


enrich_event.__signature__ = _mutmut_signature(x_enrich_event__mutmut_orig)
x_enrich_event__mutmut_orig.__name__ = "x_enrich_event"


# <3 🧱🤝📊🪄
