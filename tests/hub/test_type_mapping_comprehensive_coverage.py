#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for hub/type_mapping.py module."""

from __future__ import annotations

import types
import typing
from typing import Any, Optional, Union

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch

from provide.foundation.hub.type_mapping import extract_click_type


class TestExtractClickTypeBasicTypes(FoundationTestCase):
    """Test extract_click_type with basic types."""

    def test_extract_string_type(self) -> None:
        """Test extraction of string type."""
        result = extract_click_type(str)
        assert result is str

    def test_extract_int_type(self) -> None:
        """Test extraction of int type."""
        result = extract_click_type(int)
        assert result is int

    def test_extract_bool_type(self) -> None:
        """Test extraction of bool type."""
        result = extract_click_type(bool)
        assert result is bool

    def test_extract_float_type(self) -> None:
        """Test extraction of float type."""
        result = extract_click_type(float)
        assert result is float

    def test_extract_custom_class_type(self) -> None:
        """Test extraction of custom class type."""

        class CustomClass:
            pass

        result = extract_click_type(CustomClass)
        assert result is CustomClass


class TestExtractClickTypeNoneHandling(FoundationTestCase):
    """Test extract_click_type with None types."""

    def test_extract_none_type(self) -> None:
        """Test extraction of None type returns str."""
        result = extract_click_type(type(None))
        assert result is str

    def test_extract_nonetype_direct(self) -> None:
        """Test extraction of NoneType directly."""
        result = extract_click_type(type(None))
        assert result is str


class TestExtractClickTypeUnionTypes(FoundationTestCase):
    """Test extract_click_type with Union types."""

    def test_extract_union_str_none(self) -> None:
        """Test extraction from Union[str, None]."""
        result = extract_click_type(Union[str, None])
        assert result is str

    def test_extract_union_int_none(self) -> None:
        """Test extraction from Union[int, None]."""
        result = extract_click_type(Union[int, None])
        assert result is int

    def test_extract_union_none_str(self) -> None:
        """Test extraction from Union[None, str] (reversed order)."""
        result = extract_click_type(Union[None, str])
        assert result is str

    def test_extract_union_multiple_types(self) -> None:
        """Test extraction from Union with multiple non-None types."""
        result = extract_click_type(Union[str, int, float])
        assert result is str  # Should return first non-None type

    def test_extract_union_multiple_with_none(self) -> None:
        """Test extraction from Union with multiple types including None."""
        result = extract_click_type(Union[str, int, None])
        assert result is str  # Should return first non-None type

    def test_extract_union_only_none(self) -> None:
        """Test extraction from Union containing only None types."""
        result = extract_click_type(Union[None, type(None)])
        assert result is str  # Should default to str


class TestExtractClickTypeOptionalTypes(FoundationTestCase):
    """Test extract_click_type with Optional types."""

    def test_extract_optional_str(self) -> None:
        """Test extraction from Optional[str]."""
        result = extract_click_type(Optional[str])
        assert result is str

    def test_extract_optional_int(self) -> None:
        """Test extraction from Optional[int]."""
        result = extract_click_type(Optional[int])
        assert result is int

    def test_extract_optional_bool(self) -> None:
        """Test extraction from Optional[bool]."""
        result = extract_click_type(Optional[bool])
        assert result is bool

    def test_extract_optional_custom_type(self) -> None:
        """Test extraction from Optional[CustomType]."""

        class CustomType:
            pass

        result = extract_click_type(Optional[CustomType])
        assert result is CustomType


class TestExtractClickTypeModernUnionSyntax(FoundationTestCase):
    """Test extract_click_type with Python 3.10+ union syntax."""

    def test_extract_modern_union_str_none(self) -> None:
        """Test extraction from str | None."""
        # Use eval to avoid syntax errors in older Python versions
        annotation = eval("str | None")
        result = extract_click_type(annotation)
        assert result is str

    def test_extract_modern_union_int_none(self) -> None:
        """Test extraction from int | None."""
        annotation = eval("int | None")
        result = extract_click_type(annotation)
        assert result is int

    def test_extract_modern_union_multiple(self) -> None:
        """Test extraction from str | int | float."""
        annotation = eval("str | int | float")
        result = extract_click_type(annotation)
        assert result is str  # Should return first type

    def test_extract_modern_union_with_none(self) -> None:
        """Test extraction from str | int | None."""
        annotation = eval("str | int | None")
        result = extract_click_type(annotation)
        assert result is str  # Should return first non-None type


class TestExtractClickTypeUnionTypeDetection(FoundationTestCase):
    """Test Union type detection logic."""

    def test_typing_union_detection(self) -> None:
        """Test detection of typing.Union."""
        from typing import get_origin

        union_annotation = Union[str, int]
        origin = get_origin(union_annotation)

        assert origin is typing.Union

    def test_types_union_detection(self) -> None:
        """Test detection of types.UnionType (Python 3.10+)."""
        union_annotation = eval("str | int")
        assert isinstance(union_annotation, types.UnionType)

    def test_union_args_extraction(self) -> None:
        """Test extraction of union arguments."""
        from typing import get_args

        union_annotation = Union[str, int, None]
        args = get_args(union_annotation)

        assert str in args
        assert int in args
        assert type(None) in args


class TestExtractClickTypeEdgeCases(FoundationTestCase):
    """Test edge cases and error conditions."""

    def test_extract_any_type(self) -> None:
        """Test extraction of Any type."""
        result = extract_click_type(Any)
        assert result is Any

    def test_extract_none_args_union(self) -> None:
        """Test union with no args."""

        # Mock a union-like type with no args
        class MockUnion:
            pass

        # Mock get_origin and get_args to simulate edge case
        with (
            patch(
                "provide.foundation.parsers.typed.get_origin",
                return_value=typing.Union,
            ),
            patch("provide.foundation.parsers.typed.get_args", return_value=()),
        ):
            result = extract_click_type(MockUnion)
            # Should return str as safe default when union has no args
            assert result is str

    def test_extract_union_args_attribute(self) -> None:
        """Test union with __args__ attribute."""

        class MockUnionWithArgs:
            __args__ = (str, int, None)

        # Mock to simulate Python 3.10+ union
        with (
            patch(
                "provide.foundation.parsers.typed.get_origin",
                return_value=typing.Union,
            ),
            patch("provide.foundation.parsers.typed.get_args", return_value=()),
        ):
            # Should use __args__ when available
            mock_union = MockUnionWithArgs()
            result = extract_click_type(mock_union)
            assert result is str  # First non-None type

    def test_extract_union_all_none_types(self) -> None:
        """Test union containing only None-equivalent types."""
        # Create a mock annotation with only None types
        with (
            patch(
                "provide.foundation.parsers.typed.get_origin",
                return_value=typing.Union,
            ),
            patch(
                "provide.foundation.parsers.typed.get_args",
                return_value=(type(None), type(None)),
            ),
        ):
            result = extract_click_type("mock_annotation")
            assert result is str  # Should default to str

    def test_extract_empty_union_args(self) -> None:
        """Test union with empty args list."""
        with (
            patch(
                "provide.foundation.parsers.typed.get_origin",
                return_value=typing.Union,
            ),
            patch("provide.foundation.parsers.typed.get_args", return_value=()),
        ):
            result = extract_click_type("mock_annotation")
            # Should return str as safe default when union has no args
            assert result is str

    def test_extract_non_generic_type(self) -> None:
        """Test extraction of non-generic types."""
        # Test with a type that has no origin (non-generic)
        result = extract_click_type(list)
        assert result is list

    def test_extract_complex_generic_type(self) -> None:
        """Test extraction of complex generic types that aren't unions."""
        # These should be returned as-is since they're not unions
        result_list = extract_click_type(list[str])
        result_dict = extract_click_type(dict[str, int])

        assert result_list == list[str]
        assert result_dict == dict[str, int]


class TestExtractClickTypeUnionTypeComparisons(FoundationTestCase):
    """Test UnionType detection and comparison logic."""

    def test_union_type_isinstance_check(self) -> None:
        """Test isinstance check for UnionType."""
        union_annotation = str | int
        assert isinstance(union_annotation, types.UnionType)

    def test_union_type_hasattr_check(self) -> None:
        """Test hasattr check for UnionType."""
        # Python 3.11+ always has types.UnionType
        assert hasattr(types, "UnionType")

    def test_union_detection_logic_coverage(self) -> None:
        """Test the complete union detection logic."""
        # Test the compound condition in the function
        union_annotation = Union[str, None]
        origin = typing.get_origin(union_annotation)

        # First condition: origin is typing.Union
        assert origin is typing.Union

        # Python 3.10+ style union syntax
        modern_union = str | None
        assert isinstance(modern_union, types.UnionType)


class TestModuleExports(FoundationTestCase):
    """Test module exports and structure."""

    def test_all_exports_defined(self) -> None:
        """Test that __all__ is properly defined."""
        from provide.foundation.hub.type_mapping import __all__

        expected_exports = ["extract_click_type"]
        assert __all__ == expected_exports

    def test_all_exports_accessible(self) -> None:
        """Test that all exported items are accessible."""
        import provide.foundation.hub.type_mapping as type_mapping_module

        for export_name in type_mapping_module.__all__:
            assert hasattr(type_mapping_module, export_name)
            export_item = getattr(type_mapping_module, export_name)
            assert export_item is not None

    def test_extract_click_type_is_function(self) -> None:
        """Test that extract_click_type is a callable function."""
        assert callable(extract_click_type)

    def test_module_docstring(self) -> None:
        """Test that module has appropriate docstring."""
        import provide.foundation.hub.type_mapping as type_mapping_module

        assert type_mapping_module.__doc__ is not None
        assert "Type system" in type_mapping_module.__doc__
        assert "Click type mapping" in type_mapping_module.__doc__


class TestTypeMappingIntegration(FoundationTestCase):
    """Test integration aspects of type mapping."""

    def test_extract_click_type_with_real_function_annotations(self) -> None:
        """Test extract_click_type with real function type annotations."""

        def example_function(
            name: str,
            count: int,
            enabled: bool,
            optional_value: str | None,
            union_value: str | int,
        ) -> None:
            pass

        # Get annotations from the function
        annotations = example_function.__annotations__

        # Test each annotation
        assert extract_click_type(annotations["name"]) is str
        assert extract_click_type(annotations["count"]) is int
        assert extract_click_type(annotations["enabled"]) is bool
        assert extract_click_type(annotations["optional_value"]) is str
        assert extract_click_type(annotations["union_value"]) is str

    def test_type_mapping_consistency(self) -> None:
        """Test that type mapping is consistent across calls."""
        test_types = [str, int, bool, Optional[str], Union[str, None]]

        for test_type in test_types:
            result1 = extract_click_type(test_type)
            result2 = extract_click_type(test_type)
            assert result1 is result2

    def test_type_mapping_with_nested_annotations(self) -> None:
        """Test type mapping with nested type annotations."""
        # Test nested Optional and Union types
        nested_optional = Optional[str | int]
        result = extract_click_type(nested_optional)

        # Should extract the first non-None type from the union
        assert result in (str, int)  # Could be either depending on implementation


# 🧱🏗️🔚
