"""
pytest configuration and hooks for provide-testkit.

This module provides pytest hooks for displaying helpful information
about testkit usage without generating warnings.
"""

import os


def pytest_report_header(config):
    """Add header information to pytest output.

    This displays at the start of test sessions to inform users
    that testing helpers are active.
    """
    # Check if warnings should be suppressed
    if os.getenv("TESTKIT_SUPPRESS_WARNINGS"):
        return None

    # Only show if we appear to be in a testing context
    if not _is_testing_context():
        return None

    return [
        "",
        "⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️",
        "🚨                    PROVIDE-TESTKIT ACTIVE                    🚨",
        "🔧 Testing helpers are enabled - production behavior may differ 🔧",
        "💡 Fixtures provide automatic cleanup and isolation             💡",
        "🔇 To suppress this notice: TESTKIT_SUPPRESS_WARNINGS=1",
        "⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️",
        ""
    ]


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add footer information to pytest output.

    This displays at the end of test sessions with helpful
    reminders and links.
    """
    # Check if warnings should be suppressed
    if os.getenv("TESTKIT_SUPPRESS_WARNINGS"):
        return

    # Only show if we appear to be in a testing context
    if not _is_testing_context():
        return

    # Write footer with helpful information
    terminalreporter.write_line("")
    terminalreporter.write_line("⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️")
    terminalreporter.write_line("🚨         PROVIDE-TESTKIT SESSION COMPLETE         🚨")
    terminalreporter.write_line("✅ Test fixtures automatically cleaned up resources ✅")
    terminalreporter.write_line("🧪 All temporary files and directories removed     🧪")
    terminalreporter.write_line("📚 Documentation: https://github.com/provide-io/provide-testkit")
    terminalreporter.write_line("💡 Examples: examples/ directory in the repository 💡")
    terminalreporter.write_line("⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️")


def _is_testing_context() -> bool:
    """Detect if we're running in a testing context.

    This is the same logic used in __init__.py to determine
    when to show testing-related information.
    """
    import sys

    return (
        "pytest" in sys.modules
        or os.getenv("PYTEST_CURRENT_TEST") is not None
        or "unittest" in sys.modules
        or os.getenv("TESTING") == "true"
        or any(arg.endswith(("pytest", "py.test")) for arg in sys.argv)
    )