from __future__ import annotations

from pathlib import Path

from provide.foundation.crypto.algorithms import DEFAULT_ALGORITHM
from provide.foundation.crypto.hashing import hash_data, hash_file
from provide.foundation.crypto.utils import compare_hash
from provide.foundation.errors.resources import ResourceError
from provide.foundation.logger import get_logger

"""Checksum verification and management."""

log = get_logger(__name__)


def verify_file(
    path: Path | str,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify a file matches an expected hash.

    Args:
        path: File path
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If algorithm is not supported

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        actual_hash = hash_file(path, algorithm)
        matches = compare_hash(actual_hash, expected_hash)

        if matches:
            log.debug(
                "✅ Checksum verified",
                path=str(path),
                algorithm=algorithm,
            )
        else:
            log.warning(
                "❌ Checksum mismatch",
                path=str(path),
                algorithm=algorithm,
                expected=expected_hash[:16] + "...",
                actual=actual_hash[:16] + "...",
            )

        return matches

    except ResourceError:
        log.error(
            "❌ Failed to verify checksum - file not found",
            path=str(path),
        )
        return False


def verify_data(
    data: bytes,
    expected_hash: str,
    algorithm: str = DEFAULT_ALGORITHM,
) -> bool:
    """Verify data matches an expected hash.

    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm

    Returns:
        True if hash matches, False otherwise

    Raises:
        ValidationError: If algorithm is not supported

    """
    actual_hash = hash_data(data, algorithm)
    matches = compare_hash(actual_hash, expected_hash)

    if matches:
        log.debug(
            "✅ Data checksum verified",
            algorithm=algorithm,
            size=len(data),
        )
    else:
        log.warning(
            "❌ Data checksum mismatch",
            algorithm=algorithm,
            expected=expected_hash[:16] + "...",
            actual=actual_hash[:16] + "...",
        )

    return matches


def calculate_checksums(
    path: Path | str,
    algorithms: list[str] | None = None,
) -> dict[str, str]:
    """Calculate multiple checksums for a file.

    Args:
        path: File path
        algorithms: List of algorithms (defaults to sha256 and md5)

    Returns:
        Dictionary mapping algorithm name to hex digest

    Raises:
        ResourceError: If file cannot be read
        ValidationError: If any algorithm is not supported

    """
    if algorithms is None:
        algorithms = ["sha256", "md5"]

    from provide.foundation.crypto.hashing import hash_file_multiple

    checksums = hash_file_multiple(path, algorithms)

    log.debug(
        "📝 Calculated checksums",
        path=str(path),
        algorithms=algorithms,
    )

    return checksums


def parse_checksum_file(
    path: Path | str,
    algorithm: str | None = None,
) -> dict[str, str]:
    """Parse a checksum file and return filename to hash mapping.

    Supports common checksum file formats:
    - SHA256: "hash  filename" or "hash filename"
    - MD5: "hash  filename" or "hash filename"
    - SHA256SUMS: "hash  filename"
    - MD5SUMS: "hash  filename"

    Args:
        path: Path to checksum file
        algorithm: Expected algorithm (for validation)

    Returns:
        Dictionary mapping filename to hash

    Raises:
        ResourceError: If file cannot be read

    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise ResourceError(
            f"Checksum file not found: {path}",
            resource_type="file",
            resource_path=str(path),
        )

    checksums = {}

    try:
        from provide.foundation.file.safe import safe_read_text

        content = safe_read_text(path, default="", encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Split on whitespace (handle both single and double space)
            parts = line.split(None, 1)
            if len(parts) == 2:
                hash_value, filename = parts
                # Remove any leading asterisk (binary mode indicator)
                filename = filename.removeprefix("*")
                checksums[filename] = hash_value.lower()

        log.debug(
            "📄 Parsed checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

        return checksums

    except OSError as e:
        raise ResourceError(
            f"Failed to read checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def write_checksum_file(
    checksums: dict[str, str],
    path: Path | str,
    algorithm: str = DEFAULT_ALGORITHM,
    binary_mode: bool = True,
) -> None:
    """Write checksums to a file in standard format.

    Args:
        checksums: Dictionary mapping filename to hash
        path: Path to write checksum file
        algorithm: Algorithm name (for comments)
        binary_mode: Whether to use binary mode indicator (*)

    Raises:
        ResourceError: If file cannot be written

    """
    if isinstance(path, str):
        path = Path(path)

    try:
        from provide.foundation.file.atomic import atomic_write_text

        # Build content
        lines = [
            f"# {algorithm.upper()} checksums",
            "# Generated by provide.foundation",
            "",
        ]

        # Add checksums
        for filename, hash_value in sorted(checksums.items()):
            if binary_mode:
                lines.append(f"{hash_value}  *{filename}")
            else:
                lines.append(f"{hash_value}  {filename}")

        content = "\n".join(lines) + "\n"
        atomic_write_text(path, content, encoding="utf-8")

        log.debug(
            "📝 Wrote checksum file",
            path=str(path),
            entries=len(checksums),
            algorithm=algorithm,
        )

    except OSError as e:
        raise ResourceError(
            f"Failed to write checksum file: {path}",
            resource_type="file",
            resource_path=str(path),
        ) from e


def verify_checksum_file(
    checksum_file: Path | str,
    base_dir: Path | str | None = None,
    algorithm: str = DEFAULT_ALGORITHM,
    stop_on_error: bool = False,
) -> tuple[list[str], list[str]]:
    """Verify all files listed in a checksum file.

    Args:
        checksum_file: Path to checksum file
        base_dir: Base directory for relative paths (defaults to checksum file dir)
        algorithm: Hash algorithm to use
        stop_on_error: Whether to stop on first verification failure

    Returns:
        Tuple of (verified_files, failed_files)

    Raises:
        ResourceError: If checksum file cannot be read

    """
    if isinstance(checksum_file, str):
        checksum_file = Path(checksum_file)

    if base_dir is None:
        base_dir = checksum_file.parent
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    checksums = parse_checksum_file(checksum_file, algorithm)

    verified = []
    failed = []

    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename

        if verify_file(file_path, expected_hash, algorithm):
            verified.append(filename)
        else:
            failed.append(filename)
            if stop_on_error:
                break

    log.info(
        "📊 Checksum verification complete",
        verified=len(verified),
        failed=len(failed),
        total=len(checksums),
    )

    return verified, failed


# =============================================================================
# Prefixed Checksum Format (algorithm:hexvalue)
# =============================================================================


def format_checksum(data: bytes, algorithm: str = DEFAULT_ALGORITHM) -> str:
    """Calculate checksum with algorithm prefix.

    Returns checksums in the format "algorithm:hexdigest" (e.g., "sha256:abc123...").
    This format enables self-describing checksums that include the algorithm used.

    Args:
        data: Data to checksum
        algorithm: Hash algorithm (sha256, sha512, blake2b, blake2s, md5, adler32)

    Returns:
        Prefixed checksum string (e.g., "sha256:abc123...")

    Raises:
        ValueError: If algorithm is not supported

    Example:
        >>> data = b"Hello, World!"
        >>> format_checksum(data, "sha256")
        'sha256:dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f'
        >>> format_checksum(data, "adler32")
        'adler32:1c49043e'

    """
    if algorithm == "adler32":
        # Special case for adler32 using zlib
        import zlib

        checksum = zlib.adler32(data) & 0xFFFFFFFF
        result = f"adler32:{checksum:08x}"
        log.debug(
            "🔐 Calculated adler32 checksum",
            size=len(data),
            checksum=result,
        )
        return result

    # Use standard hashing for other algorithms
    from provide.foundation.crypto.algorithms import validate_algorithm

    validate_algorithm(algorithm)
    digest = hash_data(data, algorithm)
    result = f"{algorithm}:{digest}"

    log.debug(
        "🔐 Calculated prefixed checksum",
        algorithm=algorithm,
        size=len(data),
        checksum=result[:40] + "...",
    )

    return result


def parse_checksum(checksum_str: str) -> tuple[str, str]:
    """Parse algorithm and value from a prefixed checksum string.

    Requires prefixed format ("algorithm:hexvalue"). This enables validation
    of both the algorithm and the checksum value.

    Args:
        checksum_str: Prefixed checksum string

    Returns:
        Tuple of (algorithm, hex_value)

    Raises:
        ValueError: If checksum format is invalid or algorithm is unsupported

    Example:
        >>> parse_checksum("sha256:abc123")
        ('sha256', 'abc123')
        >>> parse_checksum("invalid")
        ValueError: Checksum must use prefixed format (algorithm:value)

    """
    if not checksum_str:
        raise ValueError("Empty checksum string")

    if ":" not in checksum_str:
        raise ValueError(f"Checksum must use prefixed format (algorithm:value): {checksum_str}")

    parts = checksum_str.split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid checksum format: {checksum_str}")

    algorithm, value = parts

    # Validate algorithm
    supported_algorithms = ["sha256", "sha512", "blake2b", "blake2s", "md5", "adler32"]
    if algorithm not in supported_algorithms:
        raise ValueError(
            f"Unknown checksum algorithm: {algorithm}. Supported: {', '.join(supported_algorithms)}"
        )

    log.debug(
        "📋 Parsed prefixed checksum",
        algorithm=algorithm,
        value=value[:16] + "...",
    )

    return algorithm, value


def verify_checksum(data: bytes, checksum_str: str) -> bool:
    """Verify data against a prefixed checksum string.

    Automatically extracts the algorithm from the checksum string and
    performs verification using the appropriate algorithm.

    Args:
        data: Data to verify
        checksum_str: Expected prefixed checksum (e.g., "sha256:abc123...")

    Returns:
        True if checksum matches, False otherwise

    Example:
        >>> data = b"test data"
        >>> checksum = format_checksum(data, "sha256")
        >>> verify_checksum(data, checksum)
        True
        >>> verify_checksum(b"wrong data", checksum)
        False

    """
    try:
        algorithm, expected_value = parse_checksum(checksum_str)
        actual_checksum = format_checksum(data, algorithm)
        actual_value = actual_checksum.split(":", 1)[1]

        matches = actual_value.lower() == expected_value.lower()

        if matches:
            log.debug(
                "✅ Prefixed checksum verified",
                algorithm=algorithm,
                size=len(data),
            )
        else:
            log.warning(
                "❌ Prefixed checksum mismatch",
                algorithm=algorithm,
                expected=expected_value[:16] + "...",
                actual=actual_value[:16] + "...",
            )

        return matches

    except (ValueError, Exception) as e:
        log.warning(
            "❌ Checksum verification failed",
            error=str(e),
            checksum=checksum_str[:40] + "...",
        )
        return False


def normalize_checksum(checksum_str: str) -> str:
    """Normalize a checksum string to prefixed format.

    Ensures the checksum is in the standard "algorithm:value" format
    and validates both the algorithm and value.

    Args:
        checksum_str: Checksum string to normalize

    Returns:
        Normalized checksum with prefix

    Raises:
        ValueError: If checksum format is invalid

    Example:
        >>> normalize_checksum("sha256:ABC123")
        'sha256:abc123'

    """
    algorithm, value = parse_checksum(checksum_str)
    normalized = f"{algorithm}:{value.lower()}"

    log.debug(
        "🔄 Normalized checksum",
        input=checksum_str[:40] + "...",
        output=normalized[:40] + "...",
    )

    return normalized


def is_strong_checksum(checksum_str: str) -> bool:
    """Check if a checksum uses a cryptographically strong algorithm.

    Strong algorithms are suitable for security-critical applications.
    Weak algorithms like MD5 and Adler32 should only be used for
    non-security purposes like data integrity checks.

    Args:
        checksum_str: Prefixed checksum string

    Returns:
        True if using a strong algorithm (sha256, sha512, blake2b, blake2s)

    Example:
        >>> is_strong_checksum("sha256:abc123")
        True
        >>> is_strong_checksum("md5:abc123")
        False
        >>> is_strong_checksum("adler32:deadbeef")
        False

    """
    try:
        algorithm, _ = parse_checksum(checksum_str)
        strong_algorithms = {"sha256", "sha512", "blake2b", "blake2s"}
        is_strong = algorithm in strong_algorithms

        log.debug(
            "🔒 Checked checksum strength",
            algorithm=algorithm,
            is_strong=is_strong,
        )

        return is_strong

    except ValueError:
        log.warning(
            "⚠️ Cannot determine checksum strength - invalid format",
            checksum=checksum_str[:40] + "...",
        )
        return False
