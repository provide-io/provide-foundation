#!/usr/bin/env bash
#
# Debug script for investigating pytest-xdist freezes
#
# This script helps diagnose where pytest-xdist workers are getting stuck
# by capturing stack traces, monitoring resources, and logging worker activity.
#
# Usage:
#   ./scripts/debug_xdist_freeze.sh [num_workers]
#
# Example:
#   ./scripts/debug_xdist_freeze.sh 4
#

set -euo pipefail

# Configuration
NUM_WORKERS="${1:-4}"
DEBUG_DIR="./debug_xdist_$(date +%Y%m%d_%H%M%S)"
PYTEST_CMD=".venv/bin/pytest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== pytest-xdist Freeze Debugger ===${NC}"
echo "Workers: $NUM_WORKERS"
echo "Debug dir: $DEBUG_DIR"
echo ""

# Create debug directory
mkdir -p "$DEBUG_DIR"

# Check if py-spy is installed (for stack traces)
if ! command -v py-spy &> /dev/null; then
    echo -e "${YELLOW}WARNING: py-spy not installed. Install with: pip install py-spy${NC}"
    echo "Stack trace collection will be skipped."
    USE_PY_SPY=false
else
    USE_PY_SPY=true
    echo -e "${GREEN}✓ py-spy found${NC}"
fi

# Function to capture worker stack traces
capture_stack_traces() {
    echo -e "${YELLOW}Capturing stack traces from workers...${NC}"

    # Find all pytest worker processes
    pids=$(pgrep -f "pytest.*worker" || true)

    if [ -z "$pids" ]; then
        echo "No worker processes found"
        return
    fi

    for pid in $pids; do
        echo "Capturing stack from PID $pid"
        if [ "$USE_PY_SPY" = true ]; then
            py-spy dump --pid "$pid" > "$DEBUG_DIR/stack_trace_$pid.txt" 2>&1 || true
        fi

        # Also capture process info
        ps -p "$pid" -o pid,ppid,state,time,command > "$DEBUG_DIR/process_info_$pid.txt" 2>&1 || true
    done

    echo -e "${GREEN}Stack traces saved to $DEBUG_DIR/${NC}"
}

# Function to monitor worker activity
monitor_workers() {
    echo -e "${YELLOW}Monitoring worker processes...${NC}"

    while true; do
        timestamp=$(date +%H:%M:%S)
        worker_count=$(pgrep -f "pytest.*worker" | wc -l)

        echo "[$timestamp] Active workers: $worker_count"

        # If workers exist, show their CPU usage
        if [ "$worker_count" -gt 0 ]; then
            ps aux | grep "pytest.*worker" | grep -v grep || true
        fi

        sleep 2
    done
}

# Function to check for freeze
check_freeze() {
    echo -e "${YELLOW}Checking for freeze pattern...${NC}"

    # Wait a bit for tests to start
    sleep 10

    # Check if progress is being made
    last_count=0
    freeze_counter=0

    while true; do
        sleep 5

        # Count passed tests in output
        current_count=$(grep -c "PASSED" "$DEBUG_DIR/pytest.log" 2>/dev/null || echo 0)

        if [ "$current_count" -eq "$last_count" ]; then
            freeze_counter=$((freeze_counter + 1))
            echo -e "${YELLOW}No progress for ${freeze_counter}x5s${NC}"

            # If no progress for 30 seconds, capture diagnostics
            if [ "$freeze_counter" -ge 6 ]; then
                echo -e "${RED}FREEZE DETECTED! Capturing diagnostics...${NC}"
                capture_stack_traces

                # Kill the monitoring loop
                pkill -P $$ monitor_workers || true

                return 1
            fi
        else
            freeze_counter=0
            echo -e "${GREEN}Progress: $current_count tests passed${NC}"
        fi

        last_count=$current_count
    done
}

# Cleanup function
cleanup() {
    echo -e "${YELLOW}Cleaning up...${NC}"

    # Kill background jobs
    jobs -p | xargs -r kill 2>/dev/null || true

    # Kill any hanging pytest workers
    pkill -f "pytest.*worker" 2>/dev/null || true

    echo "Debug artifacts saved in: $DEBUG_DIR"
    echo ""
    echo "To analyze:"
    echo "  1. Check pytest output: cat $DEBUG_DIR/pytest.log"
    echo "  2. Review stack traces: cat $DEBUG_DIR/stack_trace_*.txt"
    echo "  3. Check process info: cat $DEBUG_DIR/process_info_*.txt"
}

trap cleanup EXIT INT TERM

# Start monitoring in background
monitor_workers > "$DEBUG_DIR/worker_monitor.log" 2>&1 &
MONITOR_PID=$!

# Run pytest with xdist and capture output
echo -e "${GREEN}Starting pytest with $NUM_WORKERS workers...${NC}"
echo "Output will be saved to: $DEBUG_DIR/pytest.log"
echo ""

# Enable diagnostic logging
export PYTEST_XDIST_WORKER_DEBUG=1
export PYTEST_CONTEST_DIAG_LOG_LEVEL=DEBUG

# Run pytest with verbose output
$PYTEST_CMD \
    -n "$NUM_WORKERS" \
    -vvv \
    --log-cli-level=DEBUG \
    --tb=short \
    > "$DEBUG_DIR/pytest.log" 2>&1 &

PYTEST_PID=$!

# Start freeze detector in background
check_freeze &
FREEZE_PID=$!

# Wait for pytest to complete or freeze detector to trigger
wait $PYTEST_PID || {
    EXIT_CODE=$?
    echo -e "${RED}Pytest exited with code $EXIT_CODE${NC}"

    # Capture final diagnostics
    capture_stack_traces

    exit $EXIT_CODE
}

echo -e "${GREEN}Pytest completed successfully!${NC}"

# Kill the freeze detector
kill $FREEZE_PID 2>/dev/null || true

exit 0
