#
# env.sh
#
# Sets up the development environment for pyvider-telemetry.
# Uses 'uv' for fast virtual environment and package management.
#

# Ensure the script is run from its own directory to correctly locate .venv
ENV_SCRIPT_DIR=$(dirname "${0}")
CWD=$(pwd)

echo "ENV_SCRIPT_DIR=${ENV_SCRIPT_DIR}"
echo "CWD: ${CWD}"

if ! command -v uv >/dev/null 2>&1; then
  echo "🚀 Installing 'uv'..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source "${HOME}/.local/bin/env"
  echo "✅ 'uv' installed at $(which uv)"
  uv -V
fi

echo "🐍 Setting up Python virtual environment using uv..."

echo $(pwd)
uv venv

echo "📦 Syncing dependencies using uv..."
# Ensure all dependency groups, including 'dev', are synced.
uv sync --all-groups

echo "🔗 Activating virtual environment..."
source .venv/bin/activate

echo "🔍 Setting PYTHONPATH to include 'src' and project root..."
# Adds 'src' for package imports and project root for potential top-level scripts/modules.
export PYTHONPATH="${PWD}/src:${PWD}"

echo "✅ Environment setup complete. PYTHONPATH set to: ${PYTHONPATH}"
