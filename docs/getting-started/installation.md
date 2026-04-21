# Installation

This guide covers installing provide.foundation and setting up your development environment.

## Requirements

- **Python 3.11 or higher** - Foundation uses modern Python features
- **uv** - Package manager for installation
- **Virtual environment** (recommended) - For isolated dependencies

## Basic Installation

### Using uv (Quick install)

The simplest installation provides core logging functionality:

```bash
uv add provide-foundation
```

This installs the base package with essential dependencies:
- `structlog` - Structured logging foundation
- `attrs` - Data class utilities
- `aiofiles` - Async file I/O operations
- `tomli_w` - TOML file writing

### Using uv (Recommended for Development)

For faster dependency resolution:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Foundation
uv add provide-foundation
```

## Installation Options

Foundation offers modular installation through "extras" that add optional features:

### All Features

For the complete experience:

```bash
uv add provide-foundation[all]
```

### Specific Features

Install only what you need:

#### CLI Framework
```bash
uv add provide-foundation[cli]
```
**Adds:** `click` for command-line interface building

**Use when:** Building command-line tools, developer utilities

#### Cryptography
```bash
uv add provide-foundation[crypto]
```
**Adds:** `cryptography` library for secure operations

**Use when:** Need hashing, signatures, or certificate management

#### HTTP Transport
```bash
uv add provide-foundation[transport]
```
**Adds:** `httpx` for HTTP client operations

**Use when:** Making HTTP requests with middleware and error handling

#### OpenTelemetry
```bash
uv add provide-foundation[opentelemetry]
```
**Adds:** OpenTelemetry SDK for distributed tracing

**Use when:** Building microservices with distributed tracing needs

#### Compression
```bash
uv add provide-foundation[compression]
```
**Adds:** `zstandard` for high-performance compression

**Use when:** Need fast compression for archives and data transfer

#### Platform Utilities
```bash
uv add provide-foundation[platform]
```
**Adds:** `psutil`, `py-cpuinfo` for system information

**Use when:** Need OS/hardware detection and system monitoring

#### Process Utilities
```bash
uv add provide-foundation[process]
```
**Adds:** `psutil`, `setproctitle` for process control

**Use when:** Need process management and lifecycle control

#### Extended Utilities
```bash
uv add provide-foundation[extended]
```
**Adds:** Combination of platform and process utilities

**Use when:** Need comprehensive system-level utilities

### Combining Extras

Install multiple features:

```bash
uv add provide-foundation[cli,crypto]
```

## Virtual Environment Setup

### Using venv (Standard Library)

```bash
# Create virtual environment
python -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate

# Install Foundation
uv add provide-foundation[all]
```

### Using uv venv (Faster)

```bash
# Create and activate environment
uv venv
source .venv/bin/activate  # macOS/Linux
# or: .venv\Scripts\activate  # Windows

# Install Foundation
uv add provide-foundation[all]
```

## Verify Installation

Check that Foundation is installed correctly:

```bash
python -c "from provide.foundation import logger; logger.info('Installation successful!')"
```

You should see a formatted log message confirming the installation.

## Development Installation

For contributing to Foundation or running examples from source:

```bash
# Clone the repository
git clone https://github.com/provide-io/provide-foundation.git
cd provide-foundation

# Create virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux

# Install with development dependencies
uv sync

# Run tests to verify
pytest
```

## Dependency Overview

### Core Dependencies (Always Installed)

- **aiofiles** (>=23.2.1) - Async file I/O operations
- **attrs** (>=23.1.0) - Data class utilities
- **structlog** (>=25.3.0) - Structured logging engine
- **tomli_w** (>=1.0.0) - TOML file writing

### Optional Dependencies

| Extra | Key Dependencies | Purpose |
|-------|-----------------|---------|
| `cli` | click >=8.1.7 | CLI framework |
| `compression` | zstandard >=0.22.0 | High-performance compression |
| `crypto` | cryptography >=45.0.7 | Cryptographic operations |
| `transport` | httpx >=0.27.0 | HTTP client |
| `opentelemetry` | opentelemetry-sdk >=1.22.0 | Distributed tracing |
| `platform` | psutil, py-cpuinfo | System/OS info utilities |
| `process` | psutil, setproctitle | Process control and lifecycle |
| `extended` | (combines platform + process) | Extended system utilities |
| `all` | (all extras above) | Complete feature set |

## Platform-Specific Notes

### macOS
- Requires macOS 10.13 or higher
- Xcode Command Line Tools recommended for cryptography
- Apple Silicon (M1/M2) fully supported

### Linux
- Works on most distributions (Ubuntu, Debian, RHEL, Alpine)
- Requires `gcc` and `libffi-dev` for cryptography on some systems
- Container images: Use Python 3.11+ base images

### Windows
- Windows 10 or higher recommended
- Microsoft C++ Build Tools required for cryptography
- PowerShell or Command Prompt supported

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'provide'`

**Solution:** Ensure virtual environment is activated and Foundation is installed:
```bash
source .venv/bin/activate
uv run python -c "import importlib.metadata as m; print(m.version('provide-foundation'))"
```

### Cryptography Installation Fails

**Problem:** Build errors when installing `[crypto]` extra

**Solution:** Install platform-specific build tools:

**macOS:**
```bash
xcode-select --install
```

**Ubuntu/Debian:**
```bash
sudo apt-get install build-essential libffi-dev python3-dev
```

**RHEL/CentOS:**
```bash
sudo yum install gcc libffi-devel python3-devel
```

### Version Conflicts

**Problem:** Dependency version conflicts with existing packages

**Solution:** Use a fresh virtual environment or update conflicting packages:
```bash
uv add provide-foundation[all] --upgrade
```

## Next Steps

After installation:

1. **[Quick Start](quick-start.md)** - Write your first Foundation code
2. **[First Application](first-app.md)** - Build a complete CLI tool
3. **[Examples](examples.md)** - Explore feature-specific examples

---

**Need help?** Check the [GitHub Issues](https://github.com/provide-io/provide-foundation/issues) or ask a question.
