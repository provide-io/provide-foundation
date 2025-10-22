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
        "tests/logger/ratelimit/test_processor_ratelimiterprocessor.py",
        "tests/logger/ratelimit/test_processor_createratelimiterprocessor_ratelimiterprocessorintegration.py",
        "tests/logger/ratelimit/test_queue_limiter_queuedratelimiter.py",
        "tests/logger/ratelimit/test_queue_limiter_bufferedratelimiter_queuelimiterintegration.py",
        "tests/file/test_file_quality_qualityanalyzer.py",
        "tests/file/test_file_quality_qualityresult_operationscenario_etc.py",
        "tests/file/test_file_operations_fileevent.py",
        "tests/file/test_file_operations_operationdetector.py",
        "tests/file/test_file_operations_conveniencefunctions_fileoperation.py",
        "tests/file/test_file_operations_integration_fileoperationintegration.py",
        "tests/file/test_file_operations_integration_fileoperationsstressing.py",
        "tests/tools/test_tools_integration_downloaderintegration_backoffretryintegration.py",
        "tests/tools/test_tools_integration_fullworkflowintegration_networkerrorhandling.py",
        "tests/transport/test_transport_registry_registertransport_gettransportforscheme_etc.py",
        "tests/transport/test_transport_registry_gettransportinfo_integration.py",
        "tests/errors/test_integration_errorsystemintegration.py",
        "tests/errors/test_integration_realworldscenarios.py",
        "tests/resilience/test_retry_executor_retryexecutorsync.py",
        "tests/resilience/test_retry_executor_retryexecutorasync_retryexecutorlogging_etc.py",
    ]

    for file_path_str in broken_files:
        file_path = repo_root / file_path_str
        if file_path.exists():
            fix_broken_import(file_path)


if __name__ == "__main__":
    main()
