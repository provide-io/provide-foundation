"""Tests for archive capability system."""

import pytest
from enum import Flag, auto

from provide.foundation.archive.base import BaseArchive, ArchiveError
from provide.foundation.archive.capabilities import (
    ArchiveCapability,
    CapabilityError,
    requires_capability,
    check_capability_compatibility,
)


class TestArchiveCapabilities:
    """Test the archive capability flag system."""

    def test_archive_capability_flags(self):
        """Test that ArchiveCapability defines the expected flags."""
        # Test individual capabilities
        assert ArchiveCapability.BUNDLE
        assert ArchiveCapability.COMPRESS  
        assert ArchiveCapability.ENCRYPT
        assert ArchiveCapability.METADATA
        assert ArchiveCapability.STREAMING
        assert ArchiveCapability.DETERMINISTIC

    def test_capability_flag_combinations(self):
        """Test that capabilities can be combined using bitwise operations."""
        # Combine capabilities
        tar_caps = ArchiveCapability.BUNDLE | ArchiveCapability.METADATA
        gzip_caps = ArchiveCapability.COMPRESS | ArchiveCapability.STREAMING
        zip_caps = (ArchiveCapability.BUNDLE | 
                   ArchiveCapability.COMPRESS | 
                   ArchiveCapability.ENCRYPT | 
                   ArchiveCapability.METADATA)
        
        # Test membership
        assert ArchiveCapability.BUNDLE in tar_caps
        assert ArchiveCapability.METADATA in tar_caps
        assert ArchiveCapability.COMPRESS not in tar_caps
        
        assert ArchiveCapability.COMPRESS in gzip_caps
        assert ArchiveCapability.STREAMING in gzip_caps
        assert ArchiveCapability.BUNDLE not in gzip_caps
        
        assert ArchiveCapability.BUNDLE in zip_caps
        assert ArchiveCapability.COMPRESS in zip_caps
        assert ArchiveCapability.ENCRYPT in zip_caps

    def test_capability_validation_decorator(self):
        """Test the requires_capability decorator."""
        
        class MockArchiver(BaseArchive):
            capabilities = ArchiveCapability.BUNDLE | ArchiveCapability.METADATA
            
            @requires_capability(ArchiveCapability.BUNDLE)
            def create_bundle(self):
                return "bundled"
            
            @requires_capability(ArchiveCapability.COMPRESS)
            def compress_data(self):
                return "compressed"
            
            @requires_capability(ArchiveCapability.BUNDLE | ArchiveCapability.METADATA)
            def create_with_metadata(self):
                return "bundled with metadata"
        
        archiver = MockArchiver()
        
        # Should work - archiver has BUNDLE capability
        assert archiver.create_bundle() == "bundled"
        
        # Should work - archiver has both BUNDLE and METADATA
        assert archiver.create_with_metadata() == "bundled with metadata"
        
        # Should fail - archiver doesn't have COMPRESS capability
        with pytest.raises(CapabilityError, match="does not support required capability: COMPRESS"):
            archiver.compress_data()

    def test_capability_compatibility_checking(self):
        """Test capability compatibility between archivers."""
        tar_caps = ArchiveCapability.BUNDLE | ArchiveCapability.METADATA
        gzip_caps = ArchiveCapability.COMPRESS | ArchiveCapability.STREAMING
        zip_caps = ArchiveCapability.BUNDLE | ArchiveCapability.COMPRESS
        
        # Tar and gzip are complementary (no overlap except compatible streaming)
        assert check_capability_compatibility(tar_caps, gzip_caps) is True
        
        # Tar and zip overlap on BUNDLE - incompatible for chaining
        assert check_capability_compatibility(tar_caps, zip_caps) is False
        
        # Same capabilities are compatible
        assert check_capability_compatibility(tar_caps, tar_caps) is True


class TestCapabilitySpecificArchivers:
    """Test archivers with specific capability sets."""

    def test_tar_archiver_capabilities(self):
        """Test that TarArchive has correct capabilities."""
        from provide.foundation.archive.tar import TarArchive
        
        expected_caps = (ArchiveCapability.BUNDLE | 
                        ArchiveCapability.METADATA |
                        ArchiveCapability.STREAMING |
                        ArchiveCapability.DETERMINISTIC)
        
        assert TarArchive.capabilities == expected_caps
        
        # Should have bundling capability
        assert ArchiveCapability.BUNDLE in TarArchive.capabilities
        assert ArchiveCapability.METADATA in TarArchive.capabilities
        
        # Should NOT have compression or encryption
        assert ArchiveCapability.COMPRESS not in TarArchive.capabilities
        assert ArchiveCapability.ENCRYPT not in TarArchive.capabilities

    def test_gzip_archiver_capabilities(self):
        """Test that GzipArchive has correct capabilities.""" 
        from provide.foundation.archive.gzip import GzipArchive
        
        expected_caps = (ArchiveCapability.COMPRESS |
                        ArchiveCapability.STREAMING |
                        ArchiveCapability.DETERMINISTIC)
        
        assert GzipArchive.capabilities == expected_caps
        
        # Should have compression capability
        assert ArchiveCapability.COMPRESS in GzipArchive.capabilities
        assert ArchiveCapability.STREAMING in GzipArchive.capabilities
        
        # Should NOT have bundling or encryption
        assert ArchiveCapability.BUNDLE not in GzipArchive.capabilities
        assert ArchiveCapability.ENCRYPT not in GzipArchive.capabilities

    def test_zip_archiver_capabilities(self):
        """Test that ZipArchive has correct capabilities."""
        from provide.foundation.archive.zip import ZipArchive
        
        expected_caps = (ArchiveCapability.BUNDLE |
                        ArchiveCapability.COMPRESS |
                        ArchiveCapability.ENCRYPT |
                        ArchiveCapability.METADATA |
                        ArchiveCapability.DETERMINISTIC)
        
        assert ZipArchive.capabilities == expected_caps
        
        # Should have all major capabilities
        assert ArchiveCapability.BUNDLE in ZipArchive.capabilities
        assert ArchiveCapability.COMPRESS in ZipArchive.capabilities  
        assert ArchiveCapability.ENCRYPT in ZipArchive.capabilities
        assert ArchiveCapability.METADATA in ZipArchive.capabilities

    def test_capability_based_method_restrictions(self):
        """Test that methods are restricted based on capabilities."""
        
        class CompressionOnlyArchiver(BaseArchive):
            capabilities = ArchiveCapability.COMPRESS
            
            @requires_capability(ArchiveCapability.BUNDLE)
            def add_file(self, file_path):
                return "file added"
            
            @requires_capability(ArchiveCapability.COMPRESS) 
            def set_compression_level(self, level):
                return f"compression level set to {level}"
        
        archiver = CompressionOnlyArchiver()
        
        # Should work - has COMPRESS capability
        assert archiver.set_compression_level(9) == "compression level set to 9"
        
        # Should fail - doesn't have BUNDLE capability
        with pytest.raises(CapabilityError):
            archiver.add_file("test.txt")


class TestCapabilityInheritance:
    """Test capability inheritance and validation in class hierarchies."""

    def test_base_archiver_enforces_capabilities(self):
        """Test that BaseArchive enforces capability declarations."""
        
        # Should raise if capabilities not declared
        with pytest.raises(AttributeError):
            class NoCapsArchiver(BaseArchive):
                def create(self, source, output):
                    pass
                def extract(self, archive, output): 
                    pass
                def validate(self, archive):
                    pass
            
            # Accessing capabilities should fail
            NoCapsArchiver.capabilities

    def test_capability_validation_at_method_call(self):
        """Test that capabilities are validated at method call time."""
        
        class DynamicCapArchiver(BaseArchive):
            def __init__(self, caps):
                self.capabilities = caps
            
            @requires_capability(ArchiveCapability.COMPRESS)
            def compress(self):
                return "compressed"
        
        # Create with compression capability
        compressor = DynamicCapArchiver(ArchiveCapability.COMPRESS)
        assert compressor.compress() == "compressed"
        
        # Create without compression capability  
        bundler = DynamicCapArchiver(ArchiveCapability.BUNDLE)
        with pytest.raises(CapabilityError):
            bundler.compress()


class TestCompositeCapabilities:
    """Test how capabilities work with composite archivers."""

    def test_composite_inherits_all_capabilities(self):
        """Test that composite archivers inherit capabilities from all components."""
        from provide.foundation.archive.composite import CompositeArchive
        from provide.foundation.archive.tar import TarArchive
        from provide.foundation.archive.gzip import GzipArchive
        
        # Create tar.gz composite
        composite = CompositeArchive(TarArchive(), GzipArchive())
        
        expected_caps = (ArchiveCapability.BUNDLE |
                        ArchiveCapability.COMPRESS |
                        ArchiveCapability.METADATA |
                        ArchiveCapability.STREAMING |
                        ArchiveCapability.DETERMINISTIC)
        
        assert composite.capabilities == expected_caps
        
        # Should have capabilities from both components
        assert ArchiveCapability.BUNDLE in composite.capabilities  # from TAR
        assert ArchiveCapability.COMPRESS in composite.capabilities  # from GZIP

    def test_composite_validates_compatibility(self):
        """Test that composite validates capability compatibility."""
        from provide.foundation.archive.composite import CompositeArchive
        from provide.foundation.archive.zip import ZipArchive
        from provide.foundation.archive.tar import TarArchive
        
        # Should fail - both ZIP and TAR have BUNDLE capability
        with pytest.raises(CapabilityError, match="Conflicting capabilities"):
            CompositeArchive(TarArchive(), ZipArchive())

    def test_composite_capability_chain_validation(self):
        """Test that composite validates capability chains make sense."""
        from provide.foundation.archive.composite import CompositeArchive
        from provide.foundation.archive.gzip import GzipArchive
        
        # Should fail - can't compress nothing (gzip needs input format)
        with pytest.raises(CapabilityError, match="Invalid capability chain"):
            CompositeArchive(GzipArchive())  # Only compression, no bundle source