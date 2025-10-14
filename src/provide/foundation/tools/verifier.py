"""
Verifier Tool for Foundation.

Provides CLI commands for verifying checksums and digital signatures.
"""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Annotated

from provide.foundation.cli.helpers import (
    get_data_from_file_or_stdin,
    requires_click,
)
from provide.foundation.console.output import perr, pout
from provide.foundation.crypto import (
    Ed25519Verifier,
    parse_checksum,
    verify_checksum,
)
from provide.foundation.errors import FoundationError
from provide.foundation.hub.decorators import register_command


class VerificationError(FoundationError):
    """Raised when verification fails."""


def verify_checksum_with_hash(
    data: bytes,
    expected_hash: str,
    algorithm: str | None = None,
) -> bool:
    """Verify data against a given hash string."""
    try:
        # Normalize and parse the checksum string
        parsed_algo, parsed_hash = parse_checksum(expected_hash)
        final_algo = algorithm or parsed_algo
        return verify_checksum(data, final_algo, parsed_hash)
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
        verifier.verify(data, signature)
        return True
    except Exception as e:
        # This will catch both decoding errors and signature validation errors
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
    data, error = get_data_from_file_or_stdin(file)
    if error:
        perr(f"Error reading input: {error}", color="red")
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
    data, error = get_data_from_file_or_stdin(file)
    if error:
        perr(f"Error reading input: {error}", color="red")
        return

    try:
        if verify_signature_with_key(data, signature, key):
            pout("✓ Signature VERIFIED", color="green")
        else:
            # The function raises on failure, so this path is unlikely
            perr("✗ Signature INVALID", color="red")
    except VerificationError as e:
        perr(f"✗ Signature INVALID: {e}", color="red")
