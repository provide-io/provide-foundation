# provide/foundation/tools/verifier.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Verifier Tool for Foundation.

Provides CLI commands for verifying checksums and digital signatures.
Also provides ToolVerifier class for programmatic checksum verification.
"""

from __future__ import annotations

import base64
from pathlib import Path
import sys
from typing import Annotated

from provide.foundation.cli.helpers import requires_click
from provide.foundation.console.output import perr, pout
from provide.foundation.crypto import (
    Ed25519Verifier,
    verify_checksum,
)
from provide.foundation.crypto.hashing import hash_file
from provide.foundation.errors import FoundationError
from provide.foundation.hub.decorators import register_command
from provide.foundation.logger import get_logger

log = get_logger(__name__)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class VerificationError(FoundationError):
    """Raised when verification fails."""


class ToolVerifier:
    """Verify tool artifacts using checksums.

    Provides checksum verification for downloaded tool artifacts,
    ensuring integrity before installation.
    """

    def xǁToolVerifierǁverify_checksum__mutmut_orig(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_1(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_2(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(None)

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_3(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(None)

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_4(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if "XX:XX" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_5(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" not in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_6(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = None
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_7(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(None, 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_8(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", None)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_9(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_10(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", )
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_11(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.rsplit(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_12(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split("XX:XX", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_13(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 2)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_14(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = None
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_15(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "XXsha256XX"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_16(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "SHA256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_17(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = None

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_18(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = None

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_19(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(None, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_20(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=None)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_21(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_22(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, )

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_23(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = None

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_24(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash != expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_25(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_26(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                None,
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_27(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=None,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_28(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=None,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_29(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                algorithm=None,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_30(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                expected=expected_hash,
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_31(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                actual=actual_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_32(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                algorithm=algorithm,
            )

        return matches

    def xǁToolVerifierǁverify_checksum__mutmut_33(self, file_path: Path, expected: str) -> bool:
        """Verify file checksum.

        Args:
            file_path: Path to file to verify.
            expected: Expected checksum in format "algorithm:hash" or just "hash" (defaults to sha256).

        Returns:
            True if checksum matches, False otherwise.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If checksum format is invalid.

        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        log.debug(f"Verifying checksum for {file_path}")

        # Parse the checksum format
        if ":" in expected:
            algorithm, expected_hash = expected.split(":", 1)
        else:
            # Default to sha256 if no algorithm specified
            algorithm = "sha256"
            expected_hash = expected

        # Compute actual hash using Foundation's hash_file
        actual_hash = hash_file(file_path, algorithm=algorithm)

        matches = actual_hash == expected_hash

        if not matches:
            log.warning(
                f"Checksum mismatch for {file_path.name}",
                expected=expected_hash,
                actual=actual_hash,
                )

        return matches
    
    xǁToolVerifierǁverify_checksum__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolVerifierǁverify_checksum__mutmut_1': xǁToolVerifierǁverify_checksum__mutmut_1, 
        'xǁToolVerifierǁverify_checksum__mutmut_2': xǁToolVerifierǁverify_checksum__mutmut_2, 
        'xǁToolVerifierǁverify_checksum__mutmut_3': xǁToolVerifierǁverify_checksum__mutmut_3, 
        'xǁToolVerifierǁverify_checksum__mutmut_4': xǁToolVerifierǁverify_checksum__mutmut_4, 
        'xǁToolVerifierǁverify_checksum__mutmut_5': xǁToolVerifierǁverify_checksum__mutmut_5, 
        'xǁToolVerifierǁverify_checksum__mutmut_6': xǁToolVerifierǁverify_checksum__mutmut_6, 
        'xǁToolVerifierǁverify_checksum__mutmut_7': xǁToolVerifierǁverify_checksum__mutmut_7, 
        'xǁToolVerifierǁverify_checksum__mutmut_8': xǁToolVerifierǁverify_checksum__mutmut_8, 
        'xǁToolVerifierǁverify_checksum__mutmut_9': xǁToolVerifierǁverify_checksum__mutmut_9, 
        'xǁToolVerifierǁverify_checksum__mutmut_10': xǁToolVerifierǁverify_checksum__mutmut_10, 
        'xǁToolVerifierǁverify_checksum__mutmut_11': xǁToolVerifierǁverify_checksum__mutmut_11, 
        'xǁToolVerifierǁverify_checksum__mutmut_12': xǁToolVerifierǁverify_checksum__mutmut_12, 
        'xǁToolVerifierǁverify_checksum__mutmut_13': xǁToolVerifierǁverify_checksum__mutmut_13, 
        'xǁToolVerifierǁverify_checksum__mutmut_14': xǁToolVerifierǁverify_checksum__mutmut_14, 
        'xǁToolVerifierǁverify_checksum__mutmut_15': xǁToolVerifierǁverify_checksum__mutmut_15, 
        'xǁToolVerifierǁverify_checksum__mutmut_16': xǁToolVerifierǁverify_checksum__mutmut_16, 
        'xǁToolVerifierǁverify_checksum__mutmut_17': xǁToolVerifierǁverify_checksum__mutmut_17, 
        'xǁToolVerifierǁverify_checksum__mutmut_18': xǁToolVerifierǁverify_checksum__mutmut_18, 
        'xǁToolVerifierǁverify_checksum__mutmut_19': xǁToolVerifierǁverify_checksum__mutmut_19, 
        'xǁToolVerifierǁverify_checksum__mutmut_20': xǁToolVerifierǁverify_checksum__mutmut_20, 
        'xǁToolVerifierǁverify_checksum__mutmut_21': xǁToolVerifierǁverify_checksum__mutmut_21, 
        'xǁToolVerifierǁverify_checksum__mutmut_22': xǁToolVerifierǁverify_checksum__mutmut_22, 
        'xǁToolVerifierǁverify_checksum__mutmut_23': xǁToolVerifierǁverify_checksum__mutmut_23, 
        'xǁToolVerifierǁverify_checksum__mutmut_24': xǁToolVerifierǁverify_checksum__mutmut_24, 
        'xǁToolVerifierǁverify_checksum__mutmut_25': xǁToolVerifierǁverify_checksum__mutmut_25, 
        'xǁToolVerifierǁverify_checksum__mutmut_26': xǁToolVerifierǁverify_checksum__mutmut_26, 
        'xǁToolVerifierǁverify_checksum__mutmut_27': xǁToolVerifierǁverify_checksum__mutmut_27, 
        'xǁToolVerifierǁverify_checksum__mutmut_28': xǁToolVerifierǁverify_checksum__mutmut_28, 
        'xǁToolVerifierǁverify_checksum__mutmut_29': xǁToolVerifierǁverify_checksum__mutmut_29, 
        'xǁToolVerifierǁverify_checksum__mutmut_30': xǁToolVerifierǁverify_checksum__mutmut_30, 
        'xǁToolVerifierǁverify_checksum__mutmut_31': xǁToolVerifierǁverify_checksum__mutmut_31, 
        'xǁToolVerifierǁverify_checksum__mutmut_32': xǁToolVerifierǁverify_checksum__mutmut_32, 
        'xǁToolVerifierǁverify_checksum__mutmut_33': xǁToolVerifierǁverify_checksum__mutmut_33
    }
    
    def verify_checksum(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolVerifierǁverify_checksum__mutmut_orig"), object.__getattribute__(self, "xǁToolVerifierǁverify_checksum__mutmut_mutants"), args, kwargs, self)
        return result 
    
    verify_checksum.__signature__ = _mutmut_signature(xǁToolVerifierǁverify_checksum__mutmut_orig)
    xǁToolVerifierǁverify_checksum__mutmut_orig.__name__ = 'xǁToolVerifierǁverify_checksum'


def x__get_data_from_file_or_stdin__mutmut_orig(file_path: Path | None) -> tuple[bytes | None, str | None]:
    """Read data from a file or stdin.

    Args:
        file_path: Path to file, or None to read from stdin

    Returns:
        Tuple of (data, error_message). If successful, error_message is None.
    """
    try:
        if file_path:
            return file_path.read_bytes(), None
        else:
            # Read from stdin as bytes
            return sys.stdin.buffer.read(), None
    except Exception as e:
        return None, str(e)


def x__get_data_from_file_or_stdin__mutmut_1(file_path: Path | None) -> tuple[bytes | None, str | None]:
    """Read data from a file or stdin.

    Args:
        file_path: Path to file, or None to read from stdin

    Returns:
        Tuple of (data, error_message). If successful, error_message is None.
    """
    try:
        if file_path:
            return file_path.read_bytes(), None
        else:
            # Read from stdin as bytes
            return sys.stdin.buffer.read(), None
    except Exception as e:
        return None, str(None)

x__get_data_from_file_or_stdin__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_data_from_file_or_stdin__mutmut_1': x__get_data_from_file_or_stdin__mutmut_1
}

def _get_data_from_file_or_stdin(*args, **kwargs):
    result = _mutmut_trampoline(x__get_data_from_file_or_stdin__mutmut_orig, x__get_data_from_file_or_stdin__mutmut_mutants, args, kwargs)
    return result 

_get_data_from_file_or_stdin.__signature__ = _mutmut_signature(x__get_data_from_file_or_stdin__mutmut_orig)
x__get_data_from_file_or_stdin__mutmut_orig.__name__ = 'x__get_data_from_file_or_stdin'


def x_verify_checksum_with_hash__mutmut_orig(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_1(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = None

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_2(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["XXsha256XX", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_3(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["SHA256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_4(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "XXsha512XX", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_5(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "SHA512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_6(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "XXblake2bXX", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_7(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "BLAKE2B", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_8(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "XXblake2sXX", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_9(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "BLAKE2S", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_10(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "XXmd5XX", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_11(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "MD5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_12(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "XXadler32XX"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_13(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "ADLER32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_14(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_15(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                None
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_16(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(None)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_17(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {'XX, XX'.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_18(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = None
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_19(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif "XX:XX" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_20(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_21(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = None
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_22(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if "XX:XX" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_23(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" not in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_24(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = None
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_25(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(None, 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_26(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", None)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_27(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_28(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", )[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_29(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.rsplit(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_30(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split("XX:XX", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_31(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 2)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_32(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[1]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_33(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_34(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    None
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_35(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(None)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_36(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {'XX, XX'.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_37(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = None

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_38(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(None, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_39(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, None)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_40(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_41(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, )
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=e) from e


def x_verify_checksum_with_hash__mutmut_42(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(None, cause=e) from e


def x_verify_checksum_with_hash__mutmut_43(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", cause=None) from e


def x_verify_checksum_with_hash__mutmut_44(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(cause=e) from e


def x_verify_checksum_with_hash__mutmut_45(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string.

    Raises:
        VerificationError: If algorithm is invalid or verification fails due to error conditions
    """
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]

    # Validate algorithm first if explicitly provided
    if algorithm:
        if algorithm not in supported_algorithms:
            raise VerificationError(
                f"Checksum verification failed: Unknown checksum algorithm: {algorithm}. "
                f"Supported: {', '.join(supported_algorithms)}"
            )
        checksum_str = f"{algorithm}:{expected_hash}"
    elif ":" not in expected_hash:
        # Default to sha256 if no algorithm prefix provided
        checksum_str = f"sha256:{expected_hash}"
    else:
        # Already has algorithm prefix - validate it
        if ":" in expected_hash:
            alg = expected_hash.split(":", 1)[0]
            if alg not in supported_algorithms:
                raise VerificationError(
                    f"Checksum verification failed: Unknown checksum algorithm: {alg}. "
                    f"Supported: {', '.join(supported_algorithms)}"
                )
        checksum_str = expected_hash

    try:
        return verify_checksum(data, checksum_str)
    except Exception as e:
        raise VerificationError(f"Checksum verification failed: {e}", ) from e

x_verify_checksum_with_hash__mutmut_mutants : ClassVar[MutantDict] = {
'x_verify_checksum_with_hash__mutmut_1': x_verify_checksum_with_hash__mutmut_1, 
    'x_verify_checksum_with_hash__mutmut_2': x_verify_checksum_with_hash__mutmut_2, 
    'x_verify_checksum_with_hash__mutmut_3': x_verify_checksum_with_hash__mutmut_3, 
    'x_verify_checksum_with_hash__mutmut_4': x_verify_checksum_with_hash__mutmut_4, 
    'x_verify_checksum_with_hash__mutmut_5': x_verify_checksum_with_hash__mutmut_5, 
    'x_verify_checksum_with_hash__mutmut_6': x_verify_checksum_with_hash__mutmut_6, 
    'x_verify_checksum_with_hash__mutmut_7': x_verify_checksum_with_hash__mutmut_7, 
    'x_verify_checksum_with_hash__mutmut_8': x_verify_checksum_with_hash__mutmut_8, 
    'x_verify_checksum_with_hash__mutmut_9': x_verify_checksum_with_hash__mutmut_9, 
    'x_verify_checksum_with_hash__mutmut_10': x_verify_checksum_with_hash__mutmut_10, 
    'x_verify_checksum_with_hash__mutmut_11': x_verify_checksum_with_hash__mutmut_11, 
    'x_verify_checksum_with_hash__mutmut_12': x_verify_checksum_with_hash__mutmut_12, 
    'x_verify_checksum_with_hash__mutmut_13': x_verify_checksum_with_hash__mutmut_13, 
    'x_verify_checksum_with_hash__mutmut_14': x_verify_checksum_with_hash__mutmut_14, 
    'x_verify_checksum_with_hash__mutmut_15': x_verify_checksum_with_hash__mutmut_15, 
    'x_verify_checksum_with_hash__mutmut_16': x_verify_checksum_with_hash__mutmut_16, 
    'x_verify_checksum_with_hash__mutmut_17': x_verify_checksum_with_hash__mutmut_17, 
    'x_verify_checksum_with_hash__mutmut_18': x_verify_checksum_with_hash__mutmut_18, 
    'x_verify_checksum_with_hash__mutmut_19': x_verify_checksum_with_hash__mutmut_19, 
    'x_verify_checksum_with_hash__mutmut_20': x_verify_checksum_with_hash__mutmut_20, 
    'x_verify_checksum_with_hash__mutmut_21': x_verify_checksum_with_hash__mutmut_21, 
    'x_verify_checksum_with_hash__mutmut_22': x_verify_checksum_with_hash__mutmut_22, 
    'x_verify_checksum_with_hash__mutmut_23': x_verify_checksum_with_hash__mutmut_23, 
    'x_verify_checksum_with_hash__mutmut_24': x_verify_checksum_with_hash__mutmut_24, 
    'x_verify_checksum_with_hash__mutmut_25': x_verify_checksum_with_hash__mutmut_25, 
    'x_verify_checksum_with_hash__mutmut_26': x_verify_checksum_with_hash__mutmut_26, 
    'x_verify_checksum_with_hash__mutmut_27': x_verify_checksum_with_hash__mutmut_27, 
    'x_verify_checksum_with_hash__mutmut_28': x_verify_checksum_with_hash__mutmut_28, 
    'x_verify_checksum_with_hash__mutmut_29': x_verify_checksum_with_hash__mutmut_29, 
    'x_verify_checksum_with_hash__mutmut_30': x_verify_checksum_with_hash__mutmut_30, 
    'x_verify_checksum_with_hash__mutmut_31': x_verify_checksum_with_hash__mutmut_31, 
    'x_verify_checksum_with_hash__mutmut_32': x_verify_checksum_with_hash__mutmut_32, 
    'x_verify_checksum_with_hash__mutmut_33': x_verify_checksum_with_hash__mutmut_33, 
    'x_verify_checksum_with_hash__mutmut_34': x_verify_checksum_with_hash__mutmut_34, 
    'x_verify_checksum_with_hash__mutmut_35': x_verify_checksum_with_hash__mutmut_35, 
    'x_verify_checksum_with_hash__mutmut_36': x_verify_checksum_with_hash__mutmut_36, 
    'x_verify_checksum_with_hash__mutmut_37': x_verify_checksum_with_hash__mutmut_37, 
    'x_verify_checksum_with_hash__mutmut_38': x_verify_checksum_with_hash__mutmut_38, 
    'x_verify_checksum_with_hash__mutmut_39': x_verify_checksum_with_hash__mutmut_39, 
    'x_verify_checksum_with_hash__mutmut_40': x_verify_checksum_with_hash__mutmut_40, 
    'x_verify_checksum_with_hash__mutmut_41': x_verify_checksum_with_hash__mutmut_41, 
    'x_verify_checksum_with_hash__mutmut_42': x_verify_checksum_with_hash__mutmut_42, 
    'x_verify_checksum_with_hash__mutmut_43': x_verify_checksum_with_hash__mutmut_43, 
    'x_verify_checksum_with_hash__mutmut_44': x_verify_checksum_with_hash__mutmut_44, 
    'x_verify_checksum_with_hash__mutmut_45': x_verify_checksum_with_hash__mutmut_45
}

def verify_checksum_with_hash(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_checksum_with_hash__mutmut_orig, x_verify_checksum_with_hash__mutmut_mutants, args, kwargs)
    return result 

verify_checksum_with_hash.__signature__ = _mutmut_signature(x_verify_checksum_with_hash__mutmut_orig)
x_verify_checksum_with_hash__mutmut_orig.__name__ = 'x_verify_checksum_with_hash'


def x_verify_signature_with_key__mutmut_orig(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_1(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = None
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_2(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(None)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_3(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = None
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_4(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(None)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_5(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = None
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_6(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(None)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_7(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = None
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_8(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(None, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_9(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, None)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_10(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_11(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, )
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_12(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_13(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError(None)
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_14(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("XXSignature verification failed: Invalid signatureXX")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_15(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("signature verification failed: invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_16(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("SIGNATURE VERIFICATION FAILED: INVALID SIGNATURE")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_17(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return False
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=e) from e


def x_verify_signature_with_key__mutmut_18(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(None, cause=e) from e


def x_verify_signature_with_key__mutmut_19(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", cause=None) from e


def x_verify_signature_with_key__mutmut_20(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(cause=e) from e


def x_verify_signature_with_key__mutmut_21(
    data: bytes,
    signature_b64: str,
    public_key_b64: str,
) -> bool:
    """Verify a signature using a public key."""
    try:
        signature = base64.b64decode(signature_b64)
        public_key = base64.b64decode(public_key_b64)
        verifier = Ed25519Verifier(public_key)
        is_valid = verifier.verify(data, signature)
        if not is_valid:
            raise VerificationError("Signature verification failed: Invalid signature")
        return True
    except VerificationError:
        # Re-raise VerificationError as-is
        raise
    except Exception as e:
        # This will catch decoding errors and other exceptions
        raise VerificationError(f"Signature verification failed: {e}", ) from e

x_verify_signature_with_key__mutmut_mutants : ClassVar[MutantDict] = {
'x_verify_signature_with_key__mutmut_1': x_verify_signature_with_key__mutmut_1, 
    'x_verify_signature_with_key__mutmut_2': x_verify_signature_with_key__mutmut_2, 
    'x_verify_signature_with_key__mutmut_3': x_verify_signature_with_key__mutmut_3, 
    'x_verify_signature_with_key__mutmut_4': x_verify_signature_with_key__mutmut_4, 
    'x_verify_signature_with_key__mutmut_5': x_verify_signature_with_key__mutmut_5, 
    'x_verify_signature_with_key__mutmut_6': x_verify_signature_with_key__mutmut_6, 
    'x_verify_signature_with_key__mutmut_7': x_verify_signature_with_key__mutmut_7, 
    'x_verify_signature_with_key__mutmut_8': x_verify_signature_with_key__mutmut_8, 
    'x_verify_signature_with_key__mutmut_9': x_verify_signature_with_key__mutmut_9, 
    'x_verify_signature_with_key__mutmut_10': x_verify_signature_with_key__mutmut_10, 
    'x_verify_signature_with_key__mutmut_11': x_verify_signature_with_key__mutmut_11, 
    'x_verify_signature_with_key__mutmut_12': x_verify_signature_with_key__mutmut_12, 
    'x_verify_signature_with_key__mutmut_13': x_verify_signature_with_key__mutmut_13, 
    'x_verify_signature_with_key__mutmut_14': x_verify_signature_with_key__mutmut_14, 
    'x_verify_signature_with_key__mutmut_15': x_verify_signature_with_key__mutmut_15, 
    'x_verify_signature_with_key__mutmut_16': x_verify_signature_with_key__mutmut_16, 
    'x_verify_signature_with_key__mutmut_17': x_verify_signature_with_key__mutmut_17, 
    'x_verify_signature_with_key__mutmut_18': x_verify_signature_with_key__mutmut_18, 
    'x_verify_signature_with_key__mutmut_19': x_verify_signature_with_key__mutmut_19, 
    'x_verify_signature_with_key__mutmut_20': x_verify_signature_with_key__mutmut_20, 
    'x_verify_signature_with_key__mutmut_21': x_verify_signature_with_key__mutmut_21
}

def verify_signature_with_key(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_signature_with_key__mutmut_orig, x_verify_signature_with_key__mutmut_mutants, args, kwargs)
    return result 

verify_signature_with_key.__signature__ = _mutmut_signature(x_verify_signature_with_key__mutmut_orig)
x_verify_signature_with_key__mutmut_orig.__name__ = 'x_verify_signature_with_key'


@register_command("verify.checksum")
@requires_click
def verify_checksum_command(
    hash: Annotated[
        str,
        "The expected checksum hash (e.g., 'sha256:...')",
    ],
    file: Annotated[
        Path | None,
        "Path to the file to verify (reads from stdin if not provided)",
    ] = None,
    algorithm: Annotated[
        str | None,
        "Explicitly specify the hash algorithm (e.g., 'sha256')",
    ] = None,
) -> None:
    """Verify a file or stdin against a checksum."""
    data, error = _get_data_from_file_or_stdin(file)
    if error or data is None:
        perr(f"Error reading input: {error or 'No data'}", color="red")
        return

    try:
        if verify_checksum_with_hash(data, hash, algorithm):
            pout("✓ Checksum OK", color="green")
        else:
            perr("✗ Checksum MISMATCH", color="red")
    except VerificationError as e:
        perr(f"✗ Error: {e}", color="red")


@register_command("verify.signature")
@requires_click
def verify_signature_command(
    signature: Annotated[
        str,
        "The base64-encoded signature to verify",
    ],
    key: Annotated[
        str,
        "The base64-encoded public key for verification",
    ],
    file: Annotated[
        Path | None,
        "Path to the file to verify (reads from stdin if not provided)",
    ] = None,
) -> None:
    """Verify a digital signature for a file or stdin."""
    data, error = _get_data_from_file_or_stdin(file)
    if error or data is None:
        perr(f"Error reading input: {error or 'No data'}", color="red")
        return

    try:
        if verify_signature_with_key(data, signature, key):
            pout("✓ Signature VERIFIED", color="green")
        else:
            # The function raises on failure, so this path is unlikely
            perr("✗ Signature INVALID", color="red")
    except VerificationError as e:
        perr(f"✗ Signature INVALID: {e}", color="red")


# <3 🧱🤝🔧🪄
