"""Tests for the BaseArchive abstract interface."""

from abc import ABCMeta
from pathlib import Path

import pytest

from provide.foundation.archive.base import ArchiveError, BaseArchive


class TestBaseArchiveInterface:
    """Test the BaseArchive abstract interface."""

    def test_base_archive_is_abstract(self):
        """BaseArchive should be an abstract class that cannot be instantiated."""
        with pytest.raises(TypeError):
            BaseArchive()

    def test_base_archive_has_required_methods(self):
        """BaseArchive should define the required abstract methods."""
        # Check that BaseArchive has the required abstract methods
        abstract_methods = BaseArchive.__abstractmethods__
        expected_methods = {"create", "extract", "validate"}

        assert abstract_methods == expected_methods

    def test_base_archive_uses_abc_meta(self):
        """BaseArchive should use ABCMeta as its metaclass."""
        assert BaseArchive.__class__ is ABCMeta

    def test_concrete_implementation_must_implement_all_methods(self):
        """A concrete implementation must implement all abstract methods."""

        # Incomplete implementation (missing extract and validate)
        class IncompleteArchiver(BaseArchive):
            def create(self, source: Path, output: Path) -> Path:
                return output

        with pytest.raises(TypeError):
            IncompleteArchiver()

    def test_concrete_implementation_with_all_methods_works(self):
        """A concrete implementation with all methods should work."""

        class CompleteArchiver(BaseArchive):
            def create(self, source: Path, output: Path) -> Path:
                return output

            def extract(self, archive: Path, output: Path) -> Path:
                return output

            def validate(self, archive: Path) -> bool:
                return True

        # Should not raise
        archiver = CompleteArchiver()
        assert archiver is not None

    def test_archive_error_inheritance(self):
        """ArchiveError should inherit from Exception."""
        error = ArchiveError("test error")
        assert isinstance(error, Exception)
        assert str(error) == "test error"


class TestBaseArchiveCommonBehavior:
    """Test common behavior expected from BaseArchive implementations."""

    @pytest.fixture
    def mock_archiver(self):
        """Create a mock archiver for testing common behavior."""

        class MockArchiver(BaseArchive):
            def create(self, source: Path, output: Path) -> Path:
                # Mock implementation that creates an empty file
                output.touch()
                return output

            def extract(self, archive: Path, output: Path) -> Path:
                # Mock implementation that creates output directory
                output.mkdir(exist_ok=True)
                return output

            def validate(self, archive: Path) -> bool:
                # Mock validation that checks if file exists
                return archive.exists()

        return MockArchiver()

    def test_create_returns_output_path(self, mock_archiver, temp_directory):
        """The create method should return the output path."""
        temp_path = temp_directory
        source = temp_path / "source"
        source.mkdir()
        output = temp_path / "output.archive"

        result = mock_archiver.create(source, output)

        assert result == output
        assert output.exists()

    def test_extract_returns_output_path(self, mock_archiver, temp_directory):
        """The extract method should return the output path."""
        temp_path = temp_directory
        archive = temp_path / "test.archive"
        archive.touch()
        output = temp_path / "extracted"

        result = mock_archiver.extract(archive, output)

        assert result == output
        assert output.exists()

    def test_validate_returns_boolean(self, mock_archiver, temp_directory):
        """The validate method should return a boolean."""
        temp_path = temp_directory

        # Valid archive (exists)
        valid_archive = temp_path / "valid.archive"
        valid_archive.touch()
        assert mock_archiver.validate(valid_archive) is True

        # Invalid archive (doesn't exist)
        invalid_archive = temp_path / "invalid.archive"
        assert mock_archiver.validate(invalid_archive) is False

    def test_methods_accept_path_objects(self, mock_archiver, temp_directory):
        """All methods should accept Path objects as arguments."""
        temp_path = temp_directory
        source = temp_path / "source"
        source.mkdir()
        archive = temp_path / "test.archive"
        output = temp_path / "output"

        # All these should work with Path objects
        result1 = mock_archiver.create(source, archive)
        result2 = mock_archiver.extract(archive, output)
        result3 = mock_archiver.validate(archive)

        assert isinstance(result1, Path)
        assert isinstance(result2, Path)
        assert isinstance(result3, bool)

    def test_error_handling_pattern(self):
        """Test that implementations should raise ArchiveError for failures."""

        class FailingArchiver(BaseArchive):
            def create(self, source: Path, output: Path) -> Path:
                raise ArchiveError("Failed to create archive")

            def extract(self, archive: Path, output: Path) -> Path:
                raise ArchiveError("Failed to extract archive")

            def validate(self, archive: Path) -> bool:
                raise ArchiveError("Failed to validate archive")

        archiver = FailingArchiver()

        with pytest.raises(ArchiveError, match="Failed to create archive"):
            archiver.create(Path("source"), Path("output"))

        with pytest.raises(ArchiveError, match="Failed to extract archive"):
            archiver.extract(Path("archive"), Path("output"))

        with pytest.raises(ArchiveError, match="Failed to validate archive"):
            archiver.validate(Path("archive"))
