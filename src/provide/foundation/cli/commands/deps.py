"""CLI command for checking optional dependencies."""

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False

from provide.foundation.utils.deps import check_optional_deps


def _require_click():
    """Ensure click is available for CLI commands."""
    if not _HAS_CLICK:
        raise ImportError(
            "CLI commands require optional dependencies. "
            "Install with: pip install 'provide-foundation[cli]'"
        )


def _deps_command_impl(quiet: bool, check: str | None) -> None:
    """Implementation of deps command logic."""
    if check:
        from provide.foundation.utils.deps import has_dependency

        available = has_dependency(check)
        if not quiet:
            status = "✅" if available else "❌"
            print(f"{status} {check}: {'Available' if available else 'Missing'}")
            if not available:
                print(f"Install with: pip install 'provide-foundation[{check}]'")
        exit(0 if available else 1)
    else:
        # Check all dependencies
        deps = check_optional_deps(quiet=quiet, return_status=True)
        available_count = sum(1 for dep in deps if dep.available)
        total_count = len(deps)
        exit(0 if available_count == total_count else 1)


if _HAS_CLICK:

    @click.command("deps")
    @click.option(
        "--quiet", "-q", is_flag=True, help="Suppress output, just return exit code"
    )
    @click.option(
        "--check", metavar="DEPENDENCY", help="Check specific dependency only"
    )
    def deps_command(quiet: bool, check: str | None) -> None:
        """Check optional dependency status.

        Shows which optional dependencies are available and provides
        installation instructions for missing ones.

        Exit codes:
        - 0: All dependencies available (or specific one if --check used)
        - 1: Some dependencies missing (or specific one missing if --check used)
        """
        _deps_command_impl(quiet, check)
else:
    # Stub for when click is not available
    def deps_command(*args, **kwargs):
        """Deps command stub when click is not available."""
        _require_click()


# Export the command
__all__ = ["deps_command"]
