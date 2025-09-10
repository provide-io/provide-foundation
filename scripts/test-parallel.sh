#!/bin/bash
#
# Smart parallel test runner that uses a safe number of workers
# This prevents async test hanging issues with excessive parallelization
#

set -euo pipefail

# Get CPU count
CPU_COUNT=$(python -c "import multiprocessing; print(multiprocessing.cpu_count())")

# Calculate safe worker count (max 8, or CPU_COUNT/3, whichever is smaller)
SAFE_WORKERS=$((CPU_COUNT > 24 ? 8 : CPU_COUNT > 12 ? 6 : CPU_COUNT > 6 ? 4 : 2))

echo "🔧 Detected $CPU_COUNT CPUs, using $SAFE_WORKERS workers for safe async test execution"

# Run pytest with the calculated worker count
exec pytest -n "$SAFE_WORKERS" "$@"