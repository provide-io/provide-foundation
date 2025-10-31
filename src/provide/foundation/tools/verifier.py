#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Verifier Tool for Foundation.

Provides CLI commands for verifying checksums and digital signatures.
Also provides ToolVerifier class for programmatic checksum verification."""

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


class VerificationError(FoundationError):
    """Raised when verification fails."""


class ToolVerifier:
    """Verify tool artifacts using checksums.

    Provides checksum verification for downloaded tool artifacts,
    ensuring integrity before installation.
    """

    def verify_checksum(self, file_path: Path, expected: str) -> bool:
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


def _get_data_from_file_or_stdin(file_path: Path | None) -> tuple[bytes | None, str | None]:
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


def verify_checksum_with_hash(
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


def verify_signature_with_key(
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


# 🧱🏗️🔚
