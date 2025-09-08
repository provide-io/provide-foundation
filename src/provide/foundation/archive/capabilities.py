"""Archive capability system for explicit feature declaration."""

from enum import Flag, auto
from functools import wraps
from typing import Type

from provide.foundation.errors import FoundationError


class CapabilityError(FoundationError):
    """Raised when an operation requires capabilities not supported by an archiver."""
    pass


class ArchiveCapability(Flag):
    """
    Flags defining what operations an archiver can perform.
    
    This makes archiver capabilities explicit and prevents misuse.
    For example, you can't ask a gzip archiver to bundle files,
    or ask a tar archiver to compress data.
    """
    
    # Core operations
    BUNDLE = auto()          # Can combine multiple files/directories (tar, zip)
    COMPRESS = auto()        # Can compress data (gzip, bzip2, zip)
    ENCRYPT = auto()         # Can encrypt content (zip with password, gpg)
    
    # Metadata handling  
    METADATA = auto()        # Can preserve file metadata (tar, zip)
    PERMISSIONS = auto()     # Can preserve Unix permissions (tar)
    TIMESTAMPS = auto()      # Can preserve timestamps (tar, zip)
    
    # Operational features
    STREAMING = auto()       # Can operate on streams without temp files
    DETERMINISTIC = auto()   # Can create reproducible output
    INCREMENTAL = auto()     # Can add/update files in existing archive
    
    # Aliases for common combinations
    BASIC_BUNDLER = BUNDLE | METADATA | TIMESTAMPS
    FULL_ARCHIVER = BUNDLE | COMPRESS | METADATA | PERMISSIONS | TIMESTAMPS


def requires_capability(*capabilities: ArchiveCapability):
    """
    Decorator to enforce capability requirements on methods.
    
    Usage:
        class TarArchive(BaseArchive):
            capabilities = ArchiveCapability.BUNDLE | ArchiveCapability.METADATA
            
            @requires_capability(ArchiveCapability.BUNDLE)
            def add_file(self, file_path):
                # This method requires bundling capability
                pass
                
            @requires_capability(ArchiveCapability.COMPRESS)  
            def set_compression(self, level):
                # This will raise CapabilityError for TarArchive
                pass
    """
    required = ArchiveCapability(0)
    for cap in capabilities:
        required |= cap
    
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'capabilities'):
                raise CapabilityError(
                    f"{self.__class__.__name__} does not declare capabilities"
                )
            
            missing = required & ~self.capabilities
            if missing:
                missing_names = [cap.name for cap in ArchiveCapability if cap in missing]
                raise CapabilityError(
                    f"{self.__class__.__name__} does not support required capability: {', '.join(missing_names)}"
                )
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def check_capability_compatibility(*capability_sets: ArchiveCapability) -> bool:
    """
    Check if capability sets are compatible for chaining.
    
    Rules:
    - Core operations (BUNDLE, COMPRESS, ENCRYPT) should not overlap in a chain
    - Metadata capabilities can overlap (they're complementary)
    - Operational capabilities can always overlap
    
    Args:
        capability_sets: Capability sets to check for compatibility
        
    Returns:
        True if compatible, False otherwise
    """
    if len(capability_sets) < 2:
        return True
    
    # Core operations that shouldn't overlap in a chain
    core_ops = ArchiveCapability.BUNDLE | ArchiveCapability.COMPRESS | ArchiveCapability.ENCRYPT
    
    seen_core_ops = ArchiveCapability(0)
    
    for caps in capability_sets:
        current_core = caps & core_ops
        
        # Check for overlapping core operations
        if seen_core_ops & current_core:
            return False
        
        seen_core_ops |= current_core
    
    return True


def validate_capability_chain(capability_sets: list[ArchiveCapability]) -> None:
    """
    Validate that a chain of capabilities makes logical sense.
    
    Rules:
    - First archiver should have BUNDLE capability (source of data)
    - Compression/encryption should come after bundling
    - Chain should not be empty
    
    Args:
        capability_sets: Ordered list of capability sets in chain
        
    Raises:
        CapabilityError: If chain is invalid
    """
    if not capability_sets:
        raise CapabilityError("Empty capability chain")
    
    # First archiver should provide data (BUNDLE)
    if not (capability_sets[0] & ArchiveCapability.BUNDLE):
        raise CapabilityError("Invalid capability chain: first archiver must have BUNDLE capability")
    
    # Validate compatibility
    if not check_capability_compatibility(*capability_sets):
        raise CapabilityError("Conflicting capabilities in chain")


class CapabilityMixin:
    """
    Mixin to add capability validation to archiver classes.
    
    Usage:
        class TarArchive(BaseArchive, CapabilityMixin):
            capabilities = ArchiveCapability.BUNDLE | ArchiveCapability.METADATA
    """
    
    @classmethod
    def supports(cls, capability: ArchiveCapability) -> bool:
        """Check if this archiver supports a specific capability."""
        return capability in getattr(cls, 'capabilities', ArchiveCapability(0))
    
    @classmethod
    def get_capabilities(cls) -> ArchiveCapability:
        """Get all capabilities supported by this archiver."""
        return getattr(cls, 'capabilities', ArchiveCapability(0))
    
    def validate_operation(self, required_capability: ArchiveCapability) -> None:
        """Validate that this archiver can perform the required operation."""
        if not self.supports(required_capability):
            missing_names = [cap.name for cap in ArchiveCapability if cap in required_capability and cap not in self.capabilities]
            raise CapabilityError(
                f"{self.__class__.__name__} cannot perform operation requiring: {', '.join(missing_names)}"
            )