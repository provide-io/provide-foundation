"""Optional dependency checking utilities."""

from typing import NamedTuple


def _get_logger():
    """Lazy logger import to avoid circular dependencies."""
    from provide.foundation.logger import get_logger
    return get_logger(__name__)


class DependencyStatus(NamedTuple):
    """Status of an optional dependency."""

    name: str
    available: bool
    version: str | None
    description: str


def _check_click() -> DependencyStatus:
    """Check click availability."""
    try:
        import click

        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import version

            ver = version("click")
        except Exception:
            ver = "unknown"
        return DependencyStatus(
            name="click",
            available=True,
            version=ver,
            description="CLI features (console I/O, command building)",
        )
    except ImportError:
        return DependencyStatus(
            name="click",
            available=False,
            version=None,
            description="CLI features (console I/O, command building)",
        )


def _check_cryptography() -> DependencyStatus:
    """Check cryptography availability."""
    try:
        import cryptography

        return DependencyStatus(
            name="cryptography",
            available=True,
            version=cryptography.__version__,
            description="Crypto features (keys, certificates, signatures)",
        )
    except ImportError:
        return DependencyStatus(
            name="cryptography",
            available=False,
            version=None,
            description="Crypto features (keys, certificates, signatures)",
        )


def _check_opentelemetry() -> DependencyStatus:
    """Check OpenTelemetry availability."""
    try:
        import opentelemetry

        try:
            from importlib.metadata import version

            ver = version("opentelemetry-api")
        except Exception:
            ver = "unknown"
        return DependencyStatus(
            name="opentelemetry",
            available=True,
            version=ver,
            description="Enhanced telemetry and tracing",
        )
    except ImportError:
        return DependencyStatus(
            name="opentelemetry",
            available=False,
            version=None,
            description="Enhanced telemetry and tracing",
        )


def get_optional_dependencies() -> list[DependencyStatus]:
    """Get status of all optional dependencies.

    Returns:
        List of dependency status objects
    """
    return [
        _check_click(),
        _check_cryptography(),
        _check_opentelemetry(),
    ]


def check_optional_deps(
    *, quiet: bool = False, return_status: bool = False
) -> list[DependencyStatus] | None:
    """Check and display optional dependency status.

    Args:
        quiet: If True, don't print status (just return it)
        return_status: If True, return the status list

    Returns:
        Optional list of dependency statuses if return_status=True
    """
    deps = get_optional_dependencies()

    if not quiet:
        log = _get_logger()
        log.info("📦 provide-foundation Optional Dependencies Status")
        log.info("=" * 50)

        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)

        for dep in deps:
            status_icon = "✅" if dep.available else "❌"
            version_info = f" (v{dep.version})" if dep.version else ""
            log.info(f"  {status_icon} {dep.name}{version_info}")
            log.info(f"     {dep.description}")
            if not dep.available:
                log.info(
                    f"     Install with: pip install 'provide-foundation[{dep.name}]'"
                )

        log.info(
            f"📊 Summary: {available_count}/{total_count} optional dependencies available"
        )

        if available_count == total_count:
            log.info("🎉 All optional features are available!")
        elif available_count == 0:
            log.info(
                "💡 Install optional features with: pip install 'provide-foundation[all]'"
            )
        else:
            missing = [dep.name for dep in deps if not dep.available]
            log.info(f"💡 Missing features: {', '.join(missing)}")

    if return_status:
        return deps
    return None


def has_dependency(name: str) -> bool:
    """Check if a specific optional dependency is available.

    Args:
        name: Name of the dependency to check

    Returns:
        True if dependency is available
    """
    deps = get_optional_dependencies()
    for dep in deps:
        if dep.name == name:
            return dep.available
    return False


def require_dependency(name: str) -> None:
    """Require a specific optional dependency, raise ImportError if missing.

    Args:
        name: Name of the dependency to require

    Raises:
        ImportError: If dependency is not available
    """
    if not has_dependency(name):
        raise ImportError(
            f"Optional dependency '{name}' is required for this feature. "
            f"Install with: pip install 'provide-foundation[{name}]'"
        )


def get_available_features() -> dict[str, bool]:
    """Get a dictionary of available optional features.

    Returns:
        Dictionary mapping feature names to availability
    """
    deps = get_optional_dependencies()
    return {dep.name: dep.available for dep in deps}
