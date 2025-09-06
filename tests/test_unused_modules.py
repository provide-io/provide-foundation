"""Test to verify unused modules are not imported."""


class TestUnusedModules:
    """Test that unused modules are not accessible through main imports."""

    def test_utils_file_not_exported(self) -> None:
        """Test that utils.file is not exported from utils."""
        from provide.foundation import utils

        # utils.file should not be in the public API
        assert not hasattr(utils, "atomic_write")
        assert not hasattr(utils, "atomic_write_text")
        assert not hasattr(utils, "safe_delete")

    def test_file_module_exists_separately(self) -> None:
        """Test that file operations are in provide.foundation.file."""
        from provide.foundation.file import atomic_write, atomic_write_text, safe_delete

        # These should exist in the proper file module
        assert callable(atomic_write)
        assert callable(atomic_write_text)
        assert callable(safe_delete)

    def test_no_duplicate_file_utils(self) -> None:
        """Verify we don't have duplicate file utilities."""
        # This test documents that utils/file.py is unused
        # and file operations should use provide.foundation.file
        import provide.foundation.utils as utils

        # Check what's actually exported from utils
        exported = dir(utils)

        # File operations should not be in utils
        file_ops = [
            "atomic_write",
            "atomic_write_text",
            "safe_delete",
            "safe_copy",
            "safe_move",
            "get_file_info",
        ]

        for op in file_ops:
            assert op not in exported, f"{op} should not be in utils exports"
