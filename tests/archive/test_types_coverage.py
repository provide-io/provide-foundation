#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for archive/types.py.

These tests target uncovered lines and edge cases in the archive types module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.archive.types import (
    INVERSE_OPERATIONS,
    OPERATION_NAMES,
    ArchiveOperation,
    get_operation_from_string,
)


class TestArchiveOperationEnum(FoundationTestCase):
    """Test ArchiveOperation enum values."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_enum_values_are_correct(self) -> None:
        """Test all enum values match expected hex codes."""
        assert ArchiveOperation.NONE == 0x00
        assert ArchiveOperation.TAR == 0x01
        assert ArchiveOperation.GZIP == 0x10
        assert ArchiveOperation.BZIP2 == 0x13
        assert ArchiveOperation.XZ == 0x16
        assert ArchiveOperation.ZSTD == 0x1B
        assert ArchiveOperation.ZIP == 0x30

    def test_enum_names_are_correct(self) -> None:
        """Test all enum names are as expected."""
        assert ArchiveOperation.NONE.name == "NONE"
        assert ArchiveOperation.TAR.name == "TAR"
        assert ArchiveOperation.GZIP.name == "GZIP"
        assert ArchiveOperation.BZIP2.name == "BZIP2"
        assert ArchiveOperation.XZ.name == "XZ"
        assert ArchiveOperation.ZSTD.name == "ZSTD"
        assert ArchiveOperation.ZIP.name == "ZIP"

    def test_all_enum_values_accessible(self) -> None:
        """Test all enum values can be accessed."""
        # Access each value to ensure coverage
        operations = [
            ArchiveOperation.NONE,
            ArchiveOperation.TAR,
            ArchiveOperation.GZIP,
            ArchiveOperation.BZIP2,
            ArchiveOperation.XZ,
            ArchiveOperation.ZSTD,
            ArchiveOperation.ZIP,
        ]
        assert len(operations) == 7
        assert all(isinstance(op, ArchiveOperation) for op in operations)


class TestArchiveOperationFromString(FoundationTestCase):
    """Test ArchiveOperation.from_string() method."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_from_string_uppercase_names(self) -> None:
        """Test from_string with uppercase operation names."""
        assert ArchiveOperation.from_string("NONE") == ArchiveOperation.NONE
        assert ArchiveOperation.from_string("TAR") == ArchiveOperation.TAR
        assert ArchiveOperation.from_string("GZIP") == ArchiveOperation.GZIP
        assert ArchiveOperation.from_string("BZIP2") == ArchiveOperation.BZIP2
        assert ArchiveOperation.from_string("XZ") == ArchiveOperation.XZ
        assert ArchiveOperation.from_string("ZSTD") == ArchiveOperation.ZSTD
        assert ArchiveOperation.from_string("ZIP") == ArchiveOperation.ZIP

    def test_from_string_lowercase_names(self) -> None:
        """Test from_string with lowercase operation names."""
        assert ArchiveOperation.from_string("none") == ArchiveOperation.NONE
        assert ArchiveOperation.from_string("tar") == ArchiveOperation.TAR
        assert ArchiveOperation.from_string("gzip") == ArchiveOperation.GZIP
        assert ArchiveOperation.from_string("bzip2") == ArchiveOperation.BZIP2
        assert ArchiveOperation.from_string("xz") == ArchiveOperation.XZ
        assert ArchiveOperation.from_string("zstd") == ArchiveOperation.ZSTD
        assert ArchiveOperation.from_string("zip") == ArchiveOperation.ZIP

    def test_from_string_mixed_case(self) -> None:
        """Test from_string with mixed case names."""
        assert ArchiveOperation.from_string("Tar") == ArchiveOperation.TAR
        assert ArchiveOperation.from_string("GzIp") == ArchiveOperation.GZIP
        assert ArchiveOperation.from_string("BZip2") == ArchiveOperation.BZIP2

    def test_from_string_invalid_name_raises_value_error(self) -> None:
        """Test from_string raises ValueError for invalid operation names."""
        with pytest.raises(ValueError, match="Unknown archive operation: invalid"):
            ArchiveOperation.from_string("invalid")

    def test_from_string_empty_string_raises_value_error(self) -> None:
        """Test from_string raises ValueError for empty string."""
        with pytest.raises(ValueError, match="Unknown archive operation"):
            ArchiveOperation.from_string("")

    def test_from_string_numeric_string_raises_value_error(self) -> None:
        """Test from_string raises ValueError for numeric strings."""
        with pytest.raises(ValueError, match="Unknown archive operation"):
            ArchiveOperation.from_string("123")

    def test_from_string_extraction_alias_raises_value_error(self) -> None:
        """Test from_string doesn't accept extraction aliases (use get_operation_from_string for those)."""
        with pytest.raises(ValueError, match="Unknown archive operation"):
            ArchiveOperation.from_string("untar")


class TestArchiveOperationToString(FoundationTestCase):
    """Test ArchiveOperation.to_string() method."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_to_string_returns_lowercase(self) -> None:
        """Test to_string returns lowercase names."""
        assert ArchiveOperation.NONE.to_string() == "none"
        assert ArchiveOperation.TAR.to_string() == "tar"
        assert ArchiveOperation.GZIP.to_string() == "gzip"
        assert ArchiveOperation.BZIP2.to_string() == "bzip2"
        assert ArchiveOperation.XZ.to_string() == "xz"
        assert ArchiveOperation.ZSTD.to_string() == "zstd"
        assert ArchiveOperation.ZIP.to_string() == "zip"

    def test_to_string_round_trip(self) -> None:
        """Test round-trip conversion: enum -> string -> enum."""
        for operation in ArchiveOperation:
            string_name = operation.to_string()
            restored = ArchiveOperation.from_string(string_name)
            assert restored == operation


class TestInverseOperations(FoundationTestCase):
    """Test INVERSE_OPERATIONS dictionary."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_all_inverse_operations_defined(self) -> None:
        """Test all inverse operations are defined in dictionary."""
        assert ArchiveOperation.TAR in INVERSE_OPERATIONS
        assert ArchiveOperation.GZIP in INVERSE_OPERATIONS
        assert ArchiveOperation.BZIP2 in INVERSE_OPERATIONS
        assert ArchiveOperation.XZ in INVERSE_OPERATIONS
        assert ArchiveOperation.ZSTD in INVERSE_OPERATIONS
        assert ArchiveOperation.ZIP in INVERSE_OPERATIONS

    def test_inverse_operation_values(self) -> None:
        """Test inverse operation string values are correct."""
        assert INVERSE_OPERATIONS[ArchiveOperation.TAR] == "untar"
        assert INVERSE_OPERATIONS[ArchiveOperation.GZIP] == "gunzip"
        assert INVERSE_OPERATIONS[ArchiveOperation.BZIP2] == "bunzip2"
        assert INVERSE_OPERATIONS[ArchiveOperation.XZ] == "unxz"
        assert INVERSE_OPERATIONS[ArchiveOperation.ZSTD] == "unzstd"
        assert INVERSE_OPERATIONS[ArchiveOperation.ZIP] == "unzip"

    def test_none_operation_has_no_inverse(self) -> None:
        """Test NONE operation is not in inverse operations."""
        assert ArchiveOperation.NONE not in INVERSE_OPERATIONS


class TestOperationNames(FoundationTestCase):
    """Test OPERATION_NAMES dictionary."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_all_operation_names_defined(self) -> None:
        """Test all operation names are in dictionary."""
        # Compression operations
        assert "tar" in OPERATION_NAMES
        assert "gzip" in OPERATION_NAMES
        assert "bzip2" in OPERATION_NAMES
        assert "xz" in OPERATION_NAMES
        assert "zstd" in OPERATION_NAMES
        assert "zip" in OPERATION_NAMES

        # Extraction aliases
        assert "untar" in OPERATION_NAMES
        assert "gunzip" in OPERATION_NAMES
        assert "bunzip2" in OPERATION_NAMES
        assert "unxz" in OPERATION_NAMES
        assert "unzstd" in OPERATION_NAMES
        assert "unzip" in OPERATION_NAMES

    def test_operation_names_map_to_correct_enums(self) -> None:
        """Test operation names map to correct enum values."""
        assert OPERATION_NAMES["tar"] == ArchiveOperation.TAR
        assert OPERATION_NAMES["gzip"] == ArchiveOperation.GZIP
        assert OPERATION_NAMES["bzip2"] == ArchiveOperation.BZIP2
        assert OPERATION_NAMES["xz"] == ArchiveOperation.XZ
        assert OPERATION_NAMES["zstd"] == ArchiveOperation.ZSTD
        assert OPERATION_NAMES["zip"] == ArchiveOperation.ZIP

    def test_extraction_aliases_map_to_same_enums(self) -> None:
        """Test extraction aliases map to same enum as their operation."""
        assert OPERATION_NAMES["tar"] == OPERATION_NAMES["untar"]
        assert OPERATION_NAMES["gzip"] == OPERATION_NAMES["gunzip"]
        assert OPERATION_NAMES["bzip2"] == OPERATION_NAMES["bunzip2"]
        assert OPERATION_NAMES["xz"] == OPERATION_NAMES["unxz"]
        assert OPERATION_NAMES["zstd"] == OPERATION_NAMES["unzstd"]
        assert OPERATION_NAMES["zip"] == OPERATION_NAMES["unzip"]

    def test_operation_names_count(self) -> None:
        """Test expected number of operation names (6 operations + 6 extraction aliases)."""
        # We expect 12 total: 6 operations + 6 extraction aliases
        assert len(OPERATION_NAMES) == 12


class TestGetOperationFromString(FoundationTestCase):
    """Test get_operation_from_string() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_get_operation_from_string_compression_operations(self) -> None:
        """Test get_operation_from_string with compression operation names."""
        assert get_operation_from_string("tar") == ArchiveOperation.TAR
        assert get_operation_from_string("gzip") == ArchiveOperation.GZIP
        assert get_operation_from_string("bzip2") == ArchiveOperation.BZIP2
        assert get_operation_from_string("xz") == ArchiveOperation.XZ
        assert get_operation_from_string("zstd") == ArchiveOperation.ZSTD
        assert get_operation_from_string("zip") == ArchiveOperation.ZIP

    def test_get_operation_from_string_extraction_aliases(self) -> None:
        """Test get_operation_from_string with extraction aliases."""
        assert get_operation_from_string("untar") == ArchiveOperation.TAR
        assert get_operation_from_string("gunzip") == ArchiveOperation.GZIP
        assert get_operation_from_string("bunzip2") == ArchiveOperation.BZIP2
        assert get_operation_from_string("unxz") == ArchiveOperation.XZ
        assert get_operation_from_string("unzstd") == ArchiveOperation.ZSTD
        assert get_operation_from_string("unzip") == ArchiveOperation.ZIP

    def test_get_operation_from_string_case_insensitive(self) -> None:
        """Test get_operation_from_string is case insensitive."""
        assert get_operation_from_string("TAR") == ArchiveOperation.TAR
        assert get_operation_from_string("GZip") == ArchiveOperation.GZIP
        assert get_operation_from_string("UNTAR") == ArchiveOperation.TAR
        assert get_operation_from_string("GuNZiP") == ArchiveOperation.GZIP

    def test_get_operation_from_string_invalid_raises_value_error(self) -> None:
        """Test get_operation_from_string raises ValueError for invalid names."""
        with pytest.raises(ValueError, match="Unknown archive operation: invalid"):
            get_operation_from_string("invalid")

    def test_get_operation_from_string_empty_string_raises_value_error(self) -> None:
        """Test get_operation_from_string raises ValueError for empty string."""
        with pytest.raises(ValueError, match="Unknown archive operation"):
            get_operation_from_string("")

    def test_get_operation_from_string_whitespace_raises_value_error(self) -> None:
        """Test get_operation_from_string raises ValueError for whitespace."""
        with pytest.raises(ValueError, match="Unknown archive operation"):
            get_operation_from_string("   ")

    def test_get_operation_from_string_none_not_supported(self) -> None:
        """Test get_operation_from_string doesn't support NONE operation."""
        with pytest.raises(ValueError, match="Unknown archive operation"):
            get_operation_from_string("none")


class TestArchiveOperationComparison(FoundationTestCase):
    """Test ArchiveOperation enum comparison and identity."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_enum_equality(self) -> None:
        """Test enum values can be compared for equality."""
        assert ArchiveOperation.TAR == ArchiveOperation.TAR
        assert ArchiveOperation.GZIP != ArchiveOperation.BZIP2

    def test_enum_identity(self) -> None:
        """Test enum values maintain identity."""
        op1 = ArchiveOperation.TAR
        op2 = ArchiveOperation.TAR
        assert op1 is op2

    def test_enum_integer_comparison(self) -> None:
        """Test enum values can be compared to integers."""
        assert ArchiveOperation.TAR == 0x01
        assert ArchiveOperation.GZIP == 0x10
        assert ArchiveOperation.ZIP == 0x30


class TestArchiveOperationIntegration(FoundationTestCase):
    """Test integration scenarios with archive operations."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_from_string_to_string_round_trip_all_operations(self) -> None:
        """Test round-trip for all operations using from_string and to_string."""
        operation_names = ["NONE", "TAR", "GZIP", "BZIP2", "XZ", "ZSTD", "ZIP"]

        for name in operation_names:
            operation = ArchiveOperation.from_string(name)
            string_name = operation.to_string()
            restored = ArchiveOperation.from_string(string_name)
            assert restored == operation
            assert string_name == name.lower()

    def test_get_operation_from_string_with_all_aliases(self) -> None:
        """Test get_operation_from_string works with all defined aliases."""
        for op_name, expected_op in OPERATION_NAMES.items():
            result = get_operation_from_string(op_name)
            assert result == expected_op

    def test_inverse_operations_match_operation_names(self) -> None:
        """Test that inverse operation strings are in OPERATION_NAMES."""
        for operation, inverse_name in INVERSE_OPERATIONS.items():
            assert inverse_name in OPERATION_NAMES
            assert OPERATION_NAMES[inverse_name] == operation


__all__ = [
    "TestArchiveOperationComparison",
    "TestArchiveOperationEnum",
    "TestArchiveOperationFromString",
    "TestArchiveOperationIntegration",
    "TestArchiveOperationToString",
    "TestGetOperationFromString",
    "TestInverseOperations",
    "TestOperationNames",
]

# 🧱🏗️🔚
