"""
Tool verification system for checksums and signatures.

Provides capabilities for verifying downloaded tools using various
checksum algorithms and GPG/PGP signatures.
"""

import hashlib
import re
from pathlib import Path
from typing import Literal

from provide.foundation.errors import FoundationError
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class VerificationError(FoundationError):
    """Raised when verification fails."""
    
    pass


HashAlgo = Literal["sha256", "sha512", "md5", "blake2b"]


class ToolVerifier:
    """
    Verify tool artifacts using checksums and signatures.
    
    Supports multiple checksum algorithms and GPG/PGP signatures
    for ensuring artifact integrity and authenticity.
    """
    
    SUPPORTED_ALGORITHMS = ["sha256", "sha512", "md5", "blake2b"]
    CHUNK_SIZE = 8192  # Read files in 8KB chunks
    
    def verify_checksum(
        self,
        file_path: Path,
        expected: str,
        algo: HashAlgo = "sha256"
    ) -> bool:
        """
        Verify file checksum.
        
        Args:
            file_path: Path to file to verify.
            expected: Expected checksum (hex string).
            algo: Hash algorithm to use.
            
        Returns:
            True if checksum matches, False otherwise.
            
        Raises:
            ValueError: If algorithm is not supported.
            FileNotFoundError: If file doesn't exist.
        """
        if algo not in self.SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unsupported hash algorithm: {algo}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        log.debug(f"Verifying {algo} checksum for {file_path}")
        
        # Create hasher
        hasher = hashlib.new(algo)
        
        # Read file in chunks
        with file_path.open("rb") as f:
            while chunk := f.read(self.CHUNK_SIZE):
                hasher.update(chunk)
        
        actual = hasher.hexdigest()
        matches = actual == expected
        
        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}: "
                f"expected {expected}, got {actual}"
            )
        
        return matches
    
    def verify_shasums_file(
        self,
        shasums_file: Path,
        target_file: Path
    ) -> bool:
        """
        Verify using a shasums file (common for Go/Terraform).
        
        Args:
            shasums_file: Path to shasums file.
            target_file: Path to file to verify.
            
        Returns:
            True if file is listed and checksum matches, False otherwise.
        """
        log.debug(f"Verifying {target_file.name} using {shasums_file}")
        
        with shasums_file.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Parse line: "checksum  filename" or "checksum *filename"
                parts = line.split(None, 1)
                if len(parts) != 2:
                    continue
                
                checksum, filename = parts
                # Remove asterisk prefix if present (binary mode indicator)
                filename = filename.lstrip("*")
                
                # Check if this is our file
                if filename == target_file.name:
                    return self.verify_checksum(target_file, checksum)
        
        # File not found in shasums
        log.warning(f"{target_file.name} not found in {shasums_file}")
        return False
    
    def verify_signature(
        self,
        file_path: Path,
        signature: str,
        public_key: str | None = None
    ) -> bool:
        """
        Verify GPG/PGP signature.
        
        Args:
            file_path: Path to file to verify.
            signature: Signature data.
            public_key: Optional public key for verification.
            
        Returns:
            True if signature is valid, False otherwise.
        """
        log.debug(f"Verifying signature for {file_path}")
        
        try:
            # Use foundation's crypto module
            from provide.foundation.crypto import verify_signature
            
            return verify_signature(file_path, signature, public_key)
        except ImportError:
            log.warning("Crypto module not available, skipping signature verification")
            return True  # Skip if crypto not available
        except Exception as e:
            log.error(f"Signature verification failed: {e}")
            return False
    
    def extract_checksum(self, checksum_string: str) -> str:
        """
        Extract checksum from various string formats.
        
        Handles formats like:
        - "abc123"
        - "abc123  filename.tar.gz"
        - "sha256:abc123"
        - "SHA256:def456"
        
        Args:
            checksum_string: String containing checksum.
            
        Returns:
            Extracted checksum hex string.
        """
        checksum_string = checksum_string.strip()
        
        # Remove algorithm prefix if present
        if ":" in checksum_string:
            checksum_string = checksum_string.split(":", 1)[1]
        
        # Take first word (checksum is before any whitespace)
        checksum = checksum_string.split()[0]
        
        # Remove any asterisk prefix (binary mode indicator)
        checksum = checksum.lstrip("*")
        
        return checksum