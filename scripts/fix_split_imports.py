#!/usr/bin/env python3
"""Fix broken imports in split test files."""

from __future__ import annotations

import re
from pathlib import Path


# Mapping of broken import lines to their correct imports
IMPORT_FIXES = {
    "from provide.foundation.logger.ratelimit.processor import (": [
        "RateLimiterProcessor",
        "create_rate_limiter_processor",
    ],
    "from provide.foundation.logger.ratelimit.queue_limiter import (": [
        "BufferedRateLimiter",
        "QueuedRateLimiter",
    ],
    "from provide.foundation.file.operations import (": [
        "FileEvent",
        "FileOperation",
        "OperationDetector",
        "OperationScenario",
        "QualityAnalyzer",
        "QualityResult",
        "atomic_save",
        "await_file_created",
        "await_file_deleted",
        "await_file_modified",
    ],
    "from provide.foundation.tools.base import (": [
        "BaseToolManager",
        "ToolDownloader",
    ],
    "from provide.foundation.transport.registry import (": [
        "TransportRegistry",
        "get_transport_for_scheme",
        "get_transport_info",
        "register_transport",
    ],
    "from provide.foundation import (": [
        "Hub",
        "get_hub",
    ],
    "from provide.foundation.resilience.retry import (": [
        "RetryExecutor",
        "RetryPolicy",
    ],
    "from provide.foundation.hub.commands import (": [
        "Command",
        "CommandGroup",
        "get_command",
        "register_command",
    ],
    "from provide.foundation.config.manager import (": [
        "ConfigManager",
        "get_config",
        "load_config",
        "reload_config",
    ],
    "from provide.foundation.console.output import (": [
        "pout",
        "perr",
        "get_context",
        "should_use_json",
    ],
    "from provide.foundation.errors.handlers import (": [
        "ErrorBoundary",
        "ErrorHandler",
        "TransactionalErrorBoundary",
        "create_error_handler",
        "handle_error",
    ],
    "from provide.foundation.concurrency import (": [
        "async_gather",
        "async_run_in_executor",
        "async_sleep",
        "create_task_group",
    ],
}


def fix_broken_import(file_path: Path) -> None:
    """Fix broken imports in a file."""
    content = file_path.read_text()
    lines = content.split("\n")

    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this is a broken import
        is_broken = False
        for broken_pattern, imports in IMPORT_FIXES.items():
            if line.strip() == broken_pattern:
                # Found a broken import - replace with complete import
                import_list = ",\n    ".join(imports)
                fixed_lines.append(f"{broken_pattern}")
                fixed_lines.append(f"    {import_list},")
                fixed_lines.append(")")
                is_broken = True
                break

        if not is_broken:
            fixed_lines.append(line)

        i += 1

    # Write back
    file_path.write_text("\n".join(fixed_lines))
    print(f"Fixed: {file_path}")


def main() -> None:
    """Main entry point."""
    repo_root = Path("/Users/tim/code/gh/provide-io/provide-foundation")

    broken_files = [
        "tests/hub/test_hub_nested_commands_nestedcommandregistration.py",
        "tests/hub/test_hub_nested_commands_nestedcommandintegration.py",
        "tests/config/test_config_manager_coverage_configmanagercomprehensive.py",
        "tests/config/test_config_manager_coverage_globalfunctions.py",
        "tests/console/test_console_output_coverage_getcontext_shouldusejson_etc.py",
        "tests/console/test_console_output_coverage_perrfunction_edgecases.py",
        "tests/errors/test_handlers_errorboundary_transactional_etc.py",
        "tests/errors/test_handlers_errorhandler_createerrorhandler.py",
        "tests/concurrency/test_async_core_asyncsleep_asyncgather_etc.py",
        "tests/concurrency/test_async_core_asyncutilitiesintegration.py",
        "tests/file/test_file_quality_qualityanalyzer_qualityanalyzer.py",
    ]

    for file_path_str in broken_files:
        file_path = repo_root / file_path_str
        if file_path.exists():
            fix_broken_import(file_path)


if __name__ == "__main__":
    main()
