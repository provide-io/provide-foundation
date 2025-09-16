"""Tests for documentation generation utilities."""

from pathlib import Path
import tempfile
from unittest.mock import Mock, mock_open, patch

import pytest

from provide.foundation.docs.generator import APIDocGenerator, generate_api_docs


class TestAPIDocGenerator:
    """Test cases for APIDocGenerator."""

    def test_init_default_values(self) -> None:
        """Test APIDocGenerator initialization with default values."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator()

            assert generator.src_root == Path("src")
            assert generator.api_dir == "api/reference"
            assert generator.skip_patterns == {"__pycache__", "test", "tests"}
            assert generator.package_prefix is None
            assert generator.min_init_size == 100
            assert generator.show_source is True
            assert generator.show_inheritance is True
            assert generator.custom_index_content is None

    def test_init_custom_values(self) -> None:
        """Test APIDocGenerator initialization with custom values."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            skip_patterns = {"custom", "skip"}
            custom_content = "Custom index content"

            generator = APIDocGenerator(
                src_root="custom_src",
                api_dir="custom_api",
                skip_patterns=skip_patterns,
                package_prefix="my.package",
                min_init_size=200,
                show_source=False,
                show_inheritance=False,
                custom_index_content=custom_content,
            )

            assert generator.src_root == Path("custom_src")
            assert generator.api_dir == "custom_api"
            assert generator.skip_patterns == skip_patterns
            assert generator.package_prefix == "my.package"
            assert generator.min_init_size == 200
            assert generator.show_source is False
            assert generator.show_inheritance is False
            assert generator.custom_index_content == custom_content

    def test_init_mkdocs_gen_files_unavailable(self) -> None:
        """Test APIDocGenerator raises error when mkdocs_gen_files is unavailable."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files", None):
            with pytest.raises(ImportError, match="mkdocs_gen_files is required"):
                APIDocGenerator()

    def test_should_skip_patterns(self) -> None:
        """Test should_skip method with skip patterns."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator(skip_patterns={"test", "cache"})

            # Test pattern matching
            assert generator.should_skip(Path("src/test/module.py")) is True
            assert generator.should_skip(Path("src/cache/data.py")) is True
            assert generator.should_skip(Path("src/valid/module.py")) is False

    def test_should_skip_small_init_files(self) -> None:
        """Test should_skip method with small __init__.py files."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator(min_init_size=100)

            # Mock a small __init__.py file
            small_init = Mock(spec=Path)
            small_init.name = "__init__.py"
            mock_stat = Mock()
            mock_stat.st_size = 50
            small_init.stat.return_value = mock_stat
            # Mock relative_to to return a Path-like object with parts
            mock_relative = Mock()
            mock_relative.parts = ("__init__.py",)
            small_init.relative_to.return_value = mock_relative

            # Mock a large __init__.py file
            large_init = Mock(spec=Path)
            large_init.name = "__init__.py"
            mock_stat_large = Mock()
            mock_stat_large.st_size = 150
            large_init.stat.return_value = mock_stat_large
            # Mock relative_to to return a Path-like object with parts
            mock_relative_large = Mock()
            mock_relative_large.parts = ("__init__.py",)
            large_init.relative_to.return_value = mock_relative_large

            # Mock a regular file
            regular_file = Mock(spec=Path)
            regular_file.name = "module.py"
            regular_file.relative_to.return_value.parts = ("module.py",)

            assert generator.should_skip(small_init) is True
            assert generator.should_skip(large_init) is False
            assert generator.should_skip(regular_file) is False

    def test_should_skip_private_modules(self) -> None:
        """Test should_skip method with private modules."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator(src_root="src")

            # Mock paths with private modules
            private_path = Mock(spec=Path)
            private_path.name = "module.py"
            mock_private_relative = Mock()
            mock_private_relative.parts = ("package", "_private", "module.py")
            private_path.relative_to.return_value = mock_private_relative

            # Mock paths with __init__.py (should not skip)
            init_path = Mock(spec=Path)
            init_path.name = "__init__.py"
            mock_init_stat = Mock()
            mock_init_stat.st_size = 150  # Large enough to not be skipped
            init_path.stat.return_value = mock_init_stat
            mock_init_relative = Mock()
            mock_init_relative.parts = ("package", "__init__.py")
            init_path.relative_to.return_value = mock_init_relative

            # Mock regular path
            regular_path = Mock(spec=Path)
            regular_path.name = "module.py"
            mock_regular_relative = Mock()
            mock_regular_relative.parts = ("package", "module.py")
            regular_path.relative_to.return_value = mock_regular_relative

            assert generator.should_skip(private_path) is True
            assert generator.should_skip(init_path) is False
            assert generator.should_skip(regular_path) is False

    def test_get_module_identifier_with_prefix(self) -> None:
        """Test get_module_identifier with package prefix."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator(package_prefix="my.package")

            parts = ["module", "submodule"]
            result = generator.get_module_identifier(parts)

            assert result == "my.package.module.submodule"

    def test_get_module_identifier_without_prefix(self) -> None:
        """Test get_module_identifier without package prefix."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator()

            parts = ["module", "submodule"]
            result = generator.get_module_identifier(parts)

            assert result == "module.submodule"

    def test_generate_module_doc_basic(self) -> None:
        """Test generate_module_doc with basic configuration."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_file = Mock()
            mock_mkdocs.open.return_value.__enter__.return_value = mock_file
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator()

            generator.generate_module_doc(
                doc_path=Path("api/test.md"),
                identifier="test.module",
                title="Test Module",
            )

            mock_file.write.assert_any_call("# Test Module\n\n")
            mock_file.write.assert_any_call("::: test.module\n")

    def test_generate_module_doc_with_options(self) -> None:
        """Test generate_module_doc with show options disabled."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_file = Mock()
            mock_mkdocs.open.return_value.__enter__.return_value = mock_file
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator(show_source=False, show_inheritance=False)

            generator.generate_module_doc(
                doc_path=Path("api/test.md"),
                identifier="test.module",
                title="Test Module",
            )

            mock_file.write.assert_any_call("# Test Module\n\n")
            mock_file.write.assert_any_call("::: test.module\n")
            mock_file.write.assert_any_call("    options:\n")
            mock_file.write.assert_any_call("      show_source: false\n")
            mock_file.write.assert_any_call("      show_bases: false\n")

    def test_process_python_file_regular_module(self) -> None:
        """Test process_python_file with regular Python module."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_nav = {}
            mock_mkdocs.Nav.return_value = mock_nav

            generator = APIDocGenerator(src_root="src")

            # Mock the file path
            file_path = Mock(spec=Path)
            file_path.relative_to.return_value = Path("package/module.py")

            with patch.object(generator, "generate_module_doc") as mock_generate:
                with patch.object(mock_mkdocs, "set_edit_path"):
                    generator.process_python_file(file_path)

                    # Verify navigation was updated
                    assert ("package", "module") in mock_nav
                    assert mock_nav[("package", "module")] == "api/reference/package/module.md"

                    # Verify doc generation was called
                    mock_generate.assert_called_once()

    def test_process_python_file_init_module(self) -> None:
        """Test process_python_file with __init__.py module."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_nav = {}
            mock_mkdocs.Nav.return_value = mock_nav

            generator = APIDocGenerator(src_root="src")

            # Mock the file path for __init__.py
            file_path = Mock(spec=Path)
            file_path.relative_to.return_value = Path("package/__init__.py")

            with patch.object(generator, "generate_module_doc"):
                with patch.object(mock_mkdocs, "set_edit_path"):
                    generator.process_python_file(file_path)

                    # Verify navigation was updated (without __init__ part)
                    assert ("package",) in mock_nav
                    assert mock_nav[("package",)] == "api/reference/package/index.md"

    def test_process_python_file_duplicate(self) -> None:
        """Test process_python_file skips already processed files."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            generator = APIDocGenerator()

            file_path = Mock(spec=Path)
            generator._processed_files.add(file_path)

            with patch.object(generator, "generate_module_doc") as mock_generate:
                generator.process_python_file(file_path)

                # Should not call generate_module_doc for duplicate
                mock_generate.assert_not_called()

    def test_generate_navigation(self) -> None:
        """Test generate_navigation method."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_nav = Mock()
            mock_nav.build_literate_nav.return_value = ["nav line 1", "nav line 2"]
            mock_mkdocs.Nav.return_value = mock_nav

            mock_file = Mock()
            mock_mkdocs.open.return_value.__enter__.return_value = mock_file

            generator = APIDocGenerator(api_dir="custom_api")

            generator.generate_navigation()

            mock_mkdocs.open.assert_called_once_with("custom_api/SUMMARY.md", "w")
            mock_file.writelines.assert_called_once_with(["nav line 1", "nav line 2"])

    def test_generate_index_custom_content(self) -> None:
        """Test generate_index with custom content."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            mock_file = Mock()
            mock_mkdocs.open.return_value.__enter__.return_value = mock_file

            custom_content = "Custom API documentation"
            generator = APIDocGenerator(api_dir="custom_api", custom_index_content=custom_content)

            generator.generate_index()

            mock_mkdocs.open.assert_called_once_with("custom_api/index.md", "w")
            mock_file.write.assert_called_once_with(custom_content)

    def test_generate_index_default_content(self) -> None:
        """Test generate_index with default content."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = Mock()

            mock_file = Mock()
            mock_mkdocs.open.return_value.__enter__.return_value = mock_file

            generator = APIDocGenerator(api_dir="custom_api", package_prefix="my.package")

            generator.generate_index()

            mock_mkdocs.open.assert_called_once_with("custom_api/index.md", "w")

            # Check that default content was written
            written_content = mock_file.write.call_args[0][0]
            assert "# my.package Reference" in written_content
            assert "automatically generated API documentation" in written_content

    def test_generate_full_workflow(self) -> None:
        """Test complete generate workflow."""
        with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
            mock_mkdocs.Nav.return_value = {}

            # Mock rglob to return test files
            mock_files = [
                Mock(spec=Path),
                Mock(spec=Path),
                Mock(spec=Path),  # Should be skipped
            ]

            # Configure the mocks to be sortable
            mock_files[0].__lt__ = lambda self, other: str(self) < str(other)
            mock_files[1].__lt__ = lambda self, other: str(self) < str(other)
            mock_files[2].__lt__ = lambda self, other: str(self) < str(other)

            mock_files[0].relative_to.return_value = Path("package/module1.py")
            mock_files[1].relative_to.return_value = Path("package/module2.py")
            mock_files[2].relative_to.return_value = Path("test/test_module.py")

            with patch("pathlib.Path.rglob", return_value=mock_files):
                generator = APIDocGenerator(src_root="test_src")
                with patch.object(generator, "should_skip", side_effect=[False, False, True]):
                    with patch.object(generator, "process_python_file") as mock_process:
                        with patch.object(generator, "generate_navigation") as mock_nav:
                            with patch.object(generator, "generate_index") as mock_index:
                                result = generator.generate()

                                # Verify statistics
                                assert result["total_files"] == 3
                                assert result["processed_files"] == 2
                                assert result["skipped_files"] == 1

                                # Verify methods were called
                                assert mock_process.call_count == 2
                                mock_nav.assert_called_once()
                                mock_index.assert_called_once()


class TestGenerateApiDocs:
    """Test cases for generate_api_docs convenience function."""

    def test_generate_api_docs_default_args(self) -> None:
        """Test generate_api_docs with default arguments."""
        with patch("provide.foundation.docs.generator.APIDocGenerator") as mock_class:
            mock_instance = Mock()
            mock_instance.generate.return_value = {"processed_files": 5}
            mock_class.return_value = mock_instance

            result = generate_api_docs()

            # Verify APIDocGenerator was created with defaults
            mock_class.assert_called_once_with(
                src_root="src",
                api_dir="api/reference",
                skip_patterns=None,
                package_prefix=None,
            )

            # Verify generate was called and result returned
            mock_instance.generate.assert_called_once()
            assert result == {"processed_files": 5}

    def test_generate_api_docs_custom_args(self) -> None:
        """Test generate_api_docs with custom arguments."""
        with patch("provide.foundation.docs.generator.APIDocGenerator") as mock_class:
            mock_instance = Mock()
            mock_instance.generate.return_value = {"processed_files": 10}
            mock_class.return_value = mock_instance

            skip_patterns = {"custom", "skip"}
            result = generate_api_docs(
                src_root="custom_src",
                api_dir="custom_api",
                skip_patterns=skip_patterns,
                package_prefix="my.package",
                show_source=False,
            )

            # Verify APIDocGenerator was created with custom args
            mock_class.assert_called_once_with(
                src_root="custom_src",
                api_dir="custom_api",
                skip_patterns=skip_patterns,
                package_prefix="my.package",
                show_source=False,
            )

            # Verify result
            assert result == {"processed_files": 10}


class TestAPIDocGeneratorIntegration:
    """Integration tests for APIDocGenerator."""

    def test_real_file_processing(self) -> None:
        """Test with actual temporary files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            src_dir = temp_path / "src"
            src_dir.mkdir()

            # Create test Python files
            (src_dir / "module1.py").write_text('"""Test module 1."""\nclass TestClass: pass')
            (src_dir / "__init__.py").write_text('"""Package init."""\nfrom .module1 import TestClass')

            # Create subdirectory with module
            subdir = src_dir / "subpackage"
            subdir.mkdir()
            (subdir / "module2.py").write_text('"""Test module 2."""\ndef test_function(): pass')
            (subdir / "__init__.py").write_text('"""Subpackage init."""')

            with patch("provide.foundation.docs.generator.mkdocs_gen_files") as mock_mkdocs:
                # Create a mock that behaves like both a dict and has the method
                class MockNav(dict):
                    def build_literate_nav(self):
                        return ["nav line 1", "nav line 2"]

                mock_nav = MockNav()
                mock_mkdocs.Nav.return_value = mock_nav
                mock_mkdocs.open = mock_open()
                mock_mkdocs.set_edit_path = Mock()

                generator = APIDocGenerator(src_root=str(src_dir), package_prefix="test.package")

                result = generator.generate()

                # Verify files were processed
                assert result["total_files"] == 4
                assert result["processed_files"] == 2  # Only non-init files should be processed
                assert result["skipped_files"] == 2  # The two small __init__.py files should be skipped
