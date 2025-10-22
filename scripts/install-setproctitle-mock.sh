#!/usr/bin/env bash
#
# Install setproctitle mock to prevent macOS system freezing with pytest-xdist
#
# This script creates a .pth file that loads a mock setproctitle module
# BEFORE pytest-xdist can import the real one, preventing system freezing
# on macOS when running parallel tests.

set -euo pipefail

# Find the site-packages directory in the active venv
PYTHON_BIN="${VIRTUAL_ENV:-$(dirname "$(dirname "$(command -v python)")")}/bin/python"
SITE_PACKAGES=$("$PYTHON_BIN" -c "import site; print(site.getsitepackages()[0])")

PTH_FILE="$SITE_PACKAGES/00_disable_setproctitle.pth"

echo "Installing setproctitle mock..."
echo "Target: $PTH_FILE"

# Create .pth file with inline Python code
# .pth files are processed at interpreter startup, before ANY imports
cat > "$PTH_FILE" << 'EOF'
import sys, types; _m = types.ModuleType('setproctitle'); _m.setproctitle = _m.getproctitle = _m.setthreadtitle = _m.getthreadtitle = lambda *a: None; sys.modules.setdefault('setproctitle', _m)
EOF

echo "✅ setproctitle mock installed successfully"
echo ""
echo "Verification:"
"$PYTHON_BIN" -c "import setproctitle; print('  setproctitle module:', setproctitle); print('  Is mock:', not hasattr(setproctitle, '__file__'))"
