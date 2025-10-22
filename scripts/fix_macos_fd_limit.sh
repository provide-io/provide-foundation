#!/usr/bin/env bash
#
# Fix macOS File Descriptor Limits for pytest-xdist
#
# This script increases the macOS file descriptor limit to prevent
# Terminal.app from freezing when running pytest with many workers.
#
# Issue: pytest-xdist with 24 workers needs ~360 file descriptors,
# but macOS defaults to 256, causing system-wide terminal freezing.
#

set -euo pipefail

echo "=== Fixing macOS File Descriptor Limits ==="
echo ""

# Check current limits
echo "Current limits:"
launchctl limit maxfiles
echo ""

# Set new limits (requires sudo for system-wide change)
echo "Setting new limits..."
echo "This requires sudo to modify system limits."
echo ""

# Increase soft limit to 65536 and hard limit to unlimited
sudo launchctl limit maxfiles 65536 unlimited

echo ""
echo "New limits:"
launchctl limit maxfiles
echo ""

echo "✅ File descriptor limits increased!"
echo ""
echo "IMPORTANT: You must restart Terminal.app for changes to take effect."
echo ""
echo "After restarting Terminal:"
echo "  1. Open a new terminal window"
echo "  2. Run: launchctl limit maxfiles"
echo "  3. Verify soft limit shows 65536"
echo "  4. Run: pytest -n 24"
echo ""
