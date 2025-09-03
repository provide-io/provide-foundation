#!/usr/bin/env python3
"""Test that replacements in other packages work correctly."""

import sys
from pathlib import Path
import pytest
import tempfile


def test_flavorpack_atomic_replacements(tmp_path: Path) -> None:
    """Test flavorpack atomic operations are properly replaced."""
    # Add flavorpack to path
    flavorpack_path = Path('/Users/tim/code/gh/provide-io/flavorpack/src')
    if flavorpack_path.exists():
        import importlib.util
        
        # Load the atomic module directly without importing the full package
        spec = importlib.util.spec_from_file_location(
            "flavor.utils.atomic",
            str(flavorpack_path / "flavor/utils/atomic.py")
        )
        atomic_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(atomic_module)
        
        atomic_write = atomic_module.atomic_write
        atomic_replace = atomic_module.atomic_replace
        atomic_write_text = atomic_module.atomic_write_text
        safe_unlink = atomic_module.safe_unlink
        
        # Test atomic_write
        test_file = tmp_path / 'test_atomic.bin'
        atomic_write(test_file, b'test data')
        assert test_file.read_bytes() == b'test data'
        
        # Test atomic_replace
        atomic_replace(test_file, b'replaced data')
        assert test_file.read_bytes() == b'replaced data'
        
        # Test atomic_write_text
        text_file = tmp_path / 'test_text.txt'
        atomic_write_text(text_file, 'test text')
        assert text_file.read_text() == 'test text'
        
        # Test safe_unlink
        assert safe_unlink(text_file) is True
        assert not text_file.exists()
        assert safe_unlink(text_file) is False  # Already deleted


def test_flavorpack_disk_replacements(tmp_path: Path) -> None:
    """Test flavorpack disk operations are properly replaced."""
    flavorpack_path = Path('/Users/tim/code/gh/provide-io/flavorpack/src')
    if flavorpack_path.exists():
        import importlib.util
        
        # Load the disk module directly without importing the full package
        spec = importlib.util.spec_from_file_location(
            "flavor.utils.disk",
            str(flavorpack_path / "flavor/utils/disk.py")
        )
        disk_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(disk_module)
        
        ensure_directory = disk_module.ensure_directory
        
        # Test ensure_directory
        test_dir = tmp_path / 'test_dir'
        ensure_directory(test_dir, mode=0o755)
        assert test_dir.exists()
        assert test_dir.is_dir()
        
        # Should be idempotent
        ensure_directory(test_dir, mode=0o755)
        assert test_dir.exists()


def test_wrknv_install_replacements(tmp_path: Path) -> None:
    """Test wrknv install operations are properly replaced."""
    wrknv_path = Path('/Users/tim/code/gh/provide-io/wrknv/src')
    if wrknv_path.exists():
        import importlib.util
        
        # Load the install module directly without importing the full package
        spec = importlib.util.spec_from_file_location(
            "wrknv.wenv.operations.install",
            str(wrknv_path / "wrknv/wenv/operations/install.py")
        )
        install_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(install_module)
        
        copy_file = install_module.copy_file
        ensure_directory = install_module.ensure_directory
        clean_directory = install_module.clean_directory
        get_file_size = install_module.get_file_size
        
        # Test ensure_directory
        test_dir = tmp_path / 'wrknv_dir'
        ensure_directory(test_dir, mode=0o755)
        assert test_dir.exists()
        assert test_dir.is_dir()
        
        # Test copy_file
        src_file = tmp_path / 'source.txt'
        dst_file = tmp_path / 'dest.txt'
        src_file.write_text('source content')
        
        copy_file(src_file, dst_file, preserve_permissions=True)
        assert dst_file.read_text() == 'source content'
        
        # Test get_file_size
        size = get_file_size(dst_file)
        assert size == len('source content')
        
        # Test clean_directory
        test_dir = tmp_path / 'clean_test'
        test_dir.mkdir()
        (test_dir / 'file1.txt').write_text('content1')
        (test_dir / 'file2.txt').write_text('content2')
        (test_dir / '.hidden').write_text('hidden')
        
        clean_directory(test_dir, keep_hidden=True)
        assert (test_dir / '.hidden').exists()
        assert not (test_dir / 'file1.txt').exists()
        assert not (test_dir / 'file2.txt').exists()


def test_wrknv_extract_operations(tmp_path: Path) -> None:
    """Test wrknv extract operations still work."""
    wrknv_path = Path('/Users/tim/code/gh/provide-io/wrknv/src')
    if wrknv_path.exists():
        import importlib.util
        
        # Load the install module directly without importing the full package
        spec = importlib.util.spec_from_file_location(
            "wrknv.wenv.operations.install",
            str(wrknv_path / "wrknv/wenv/operations/install.py")
        )
        install_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(install_module)
        
        extract_archive = install_module.extract_archive
        make_executable = install_module.make_executable
        import tarfile
        import zipfile
        
        # Test tar.gz extraction
        tar_path = tmp_path / 'test.tar.gz'
        extract_dir = tmp_path / 'extracted_tar'
        
        # Create a test tar.gz
        with tarfile.open(tar_path, 'w:gz') as tar:
            test_file = tmp_path / 'test_content.txt'
            test_file.write_text('tar content')
            tar.add(test_file, arcname='test_content.txt')
        
        extract_archive(tar_path, extract_dir)
        assert (extract_dir / 'test_content.txt').exists()
        assert (extract_dir / 'test_content.txt').read_text() == 'tar content'
        
        # Test zip extraction
        zip_path = tmp_path / 'test.zip'
        extract_dir_zip = tmp_path / 'extracted_zip'
        
        # Create a test zip
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            test_file = tmp_path / 'zip_content.txt'
            test_file.write_text('zip content')
            zip_file.write(test_file, arcname='zip_content.txt')
        
        extract_archive(zip_path, extract_dir_zip)
        assert (extract_dir_zip / 'zip_content.txt').exists()
        assert (extract_dir_zip / 'zip_content.txt').read_text() == 'zip content'
        
        # Test make_executable (on Unix)
        import platform
        if platform.system().lower() != 'windows':
            script_file = tmp_path / 'script.sh'
            script_file.write_text('#!/bin/bash\necho test')
            
            make_executable(script_file)
            
            import stat
            mode = script_file.stat().st_mode
            assert mode & stat.S_IXUSR  # User execute bit should be set


@pytest.mark.skipif(
    not Path('/Users/tim/code/gh/provide-io/flavorpack').exists(),
    reason="flavorpack repository not available"
)
def test_flavorpack_integration() -> None:
    """Integration test for flavorpack replacements."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        test_flavorpack_atomic_replacements(tmp_path)
        test_flavorpack_disk_replacements(tmp_path)


@pytest.mark.skipif(
    not Path('/Users/tim/code/gh/provide-io/wrknv').exists(),
    reason="wrknv repository not available"
)
def test_wrknv_integration() -> None:
    """Integration test for wrknv replacements."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        test_wrknv_install_replacements(tmp_path)
        test_wrknv_extract_operations(tmp_path)