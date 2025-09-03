# Provide-IO Ecosystem Consolidation Matrix

## Executive Summary

This document provides a detailed function-level analysis of duplicated utilities across the provide-io ecosystem (8+ repositories) with specific migration paths to consolidate functionality into `provide.foundation`. The goal is to eliminate ~2,500 lines of duplicate code, improve maintainability, and ensure consistent behavior across all projects.

## 1. Platform Detection Consolidation

### Current Duplications

| Function | Repository | Current Location | Foundation Replacement | Status |
|----------|------------|------------------|----------------------|---------|
| `get_platform_info()` | wrknv | wrknv/wenv/operations/platform.py:14 | `foundation.platform.info.get_system_info()` | ✅ Ready |
| `get_os_name()` | wrknv | wrknv/wenv/operations/platform.py:30 | `foundation.platform.detection.get_os_name()` | ✅ Ready |
| `get_architecture()` | wrknv | wrknv/wenv/operations/platform.py:49 | `foundation.platform.detection.get_arch_name()` | ✅ Ready |
| `terraform_arch()` | pyvider | pyvider/cli/context.py:13 | `foundation.platform.detection.get_arch_name()` | ✅ Ready |
| `terraform_os()` | pyvider | pyvider/cli/context.py:24 | `foundation.platform.detection.get_os_name()` | ✅ Ready |
| `is_supported_platform()` | wrknv | wrknv/wenv/operations/platform.py:72 | **GAP** - Add to foundation | ❌ Missing |
| `get_executable_extension()` | wrknv | wrknv/wenv/operations/platform.py:94 | **GAP** - Add to foundation | ❌ Missing |
| `get_archive_extension()` | wrknv | wrknv/wenv/operations/platform.py:103 | **GAP** - Add to foundation | ❌ Missing |
| `get_download_platform_mappings()` | wrknv | wrknv/wenv/operations/platform.py:133 | **GAP** - Add to foundation | ❌ Missing |

### Migration Example

```python
# OLD (wrknv)
from wrknv.wenv.operations.platform import get_platform_info
info = get_platform_info()
os_name = info["os"]
arch = info["arch"]

# NEW
from provide.foundation.platform import get_system_info
info = get_system_info()
os_name = info.os_name
arch = info.architecture
```

### Required Additions to Foundation

```python
# provide.foundation.platform.utils (NEW FILE)
def is_supported_platform(os_name: str, arch: str, supported_platforms: list[tuple[str, str]]) -> bool:
    """Check if platform/arch combination is supported."""
    pass

def get_executable_extension() -> str:
    """Get platform-specific executable extension (.exe for Windows, empty for others)."""
    pass

def get_archive_extension(preferred: str = "tar.gz") -> str:
    """Get platform-appropriate archive extension."""
    pass

def get_tool_platform_mapping(tool_name: str) -> dict[str, str]:
    """Get tool-specific platform name mappings."""
    pass
```

## 2. Process Execution Consolidation

### Current Duplications

| Function | Repository | Current Location | Foundation Replacement | Status |
|----------|------------|------------------|----------------------|---------|
| `_run_command()` | pyvider | pyvider/cli/utils.py:12 | `foundation.process.run_command()` | ✅ Ready |
| `run_command()` | flavorpack | flavor/utils/subprocess.py:17 | `foundation.process.run_command()` | ✅ Ready |
| `run_command_simple()` | flavorpack | flavor/utils/subprocess.py:81 | `foundation.process.run_command_simple()` | ✅ Ready |

### Migration Examples

```python
# OLD (pyvider)
from pyvider.cli.utils import _run_command
result = _run_command(["terraform", "init"], cwd="/path", title="Initializing")

# NEW
from provide.foundation.process import run_command
from provide.foundation import plog
plog.info("Initializing Terraform")
result = run_command(["terraform", "init"], cwd="/path", check=True)

# OLD (flavorpack)
from flavor.utils.subprocess import run_command
result = run_command(["git", "status"], capture_output=True)

# NEW
from provide.foundation.process import run_command
result = run_command(["git", "status"], capture_output=True)
```

### Gaps in Foundation

- Missing: Click-based progress indicators (can use plog instead)
- Missing: Automatic log file management (use foundation logging)

## 3. File Operations (NEW MODULE NEEDED)

### Currently Missing in Foundation

| Function | Source Repository | Source Location | Purpose | Priority |
|----------|------------------|-----------------|---------|----------|
| `atomic_write()` | flavorpack | flavor/utils/atomic.py:10 | Safe file writing with temp file | HIGH |
| `atomic_replace()` | flavorpack | flavor/utils/atomic.py:54 | Atomic file replacement | HIGH |
| `atomic_write_text()` | flavorpack | flavor/utils/atomic.py:74 | Text file atomic write | HIGH |
| `safe_unlink()` | flavorpack | flavor/utils/atomic.py:86 | Safe file deletion | MEDIUM |

### Proposed New Module

```python
# provide.foundation.utils.file (NEW MODULE)
"""Atomic and safe file operations."""

from pathlib import Path
from typing import Optional

def atomic_write(path: Path, data: bytes, mode: Optional[int] = None) -> None:
    """Write file atomically using temp file and rename."""
    pass

def atomic_replace(path: Path, data: bytes) -> None:
    """Replace existing file atomically."""
    pass

def atomic_write_text(
    path: Path, 
    text: str, 
    encoding: str = "utf-8", 
    mode: Optional[int] = None
) -> None:
    """Write text file atomically."""
    pass

def safe_unlink(path: Path) -> bool:
    """Safely delete file, returning success status."""
    pass
```

## 4. Error Handling Consolidation

### Error Class Migration Mapping

| Current Class | Repository | Location | Foundation Base Class | Migration Notes |
|---------------|------------|----------|---------------------|-----------------|
| `WrkenvError` | wrknv | wrknv/wenv/exceptions.py:12 | `FoundationError` | Add suggestion system |
| `ConfigurationError` | wrknv | wrknv/wenv/exceptions.py:27 | `foundation.errors.ConfigurationError` | ✅ Direct replacement |
| `ValidationError` | wrknv | wrknv/wenv/exceptions.py:42 | `foundation.errors.ValidationError` | ✅ Direct replacement |
| `NetworkError` | wrknv | wrknv/wenv/exceptions.py:92 | `foundation.errors.NetworkError` | ✅ Direct replacement |
| `ToolNotFoundError` | wrknv | wrknv/wenv/exceptions.py:68 | **GAP** - New subclass needed | ❌ Add to foundation |
| `PackageError` | wrknv | wrknv/wenv/exceptions.py:182 | **GAP** - New subclass needed | ❌ Add to foundation |
| `GarnishError` | garnish | garnish/errors.py:10 | `FoundationError` | Keep as domain-specific |
| `handle_error()` | garnish | garnish/errors.py:100 | Use foundation error handlers | ✅ Ready |

### Migration Example

```python
# OLD (wrknv)
from wrknv.wenv.exceptions import WrkenvError, ToolNotFoundError

class MyError(WrkenvError):
    def __init__(self, msg: str):
        super().__init__(msg, suggestion="Try installing the tool first")

# NEW
from provide.foundation.errors import FoundationError

class MyError(FoundationError):
    def __init__(self, msg: str):
        super().__init__(
            msg,
            code="TOOL_NOT_FOUND",
            context={"suggestion": "Try installing the tool first"}
        )
```

### Required Additions to Foundation

```python
# provide.foundation.errors.exceptions (ADD THESE CLASSES)

class ToolError(FoundationError):
    """Base class for tool-related errors."""
    default_code = "TOOL_ERROR"

class ToolNotFoundError(ToolError):
    """Raised when a required tool is not found."""
    default_code = "TOOL_NOT_FOUND"
    
    def __init__(
        self,
        tool_name: str,
        message: str | None = None,
        suggestion: str | None = None,
        **kwargs
    ):
        if message is None:
            message = f"Tool '{tool_name}' not found"
        super().__init__(message, tool_name=tool_name, suggestion=suggestion, **kwargs)

class PackageError(FoundationError):
    """Base class for package management errors."""
    default_code = "PACKAGE_ERROR"
```

## 5. Configuration Loading Consolidation

### Configuration Component Mapping

| Component | Repository | Location | Foundation Replacement | Gap |
|-----------|------------|----------|----------------------|-----|
| `ConfigSource` (base) | wrknv | wrknv/wenv/config.py:41 | `foundation.config.ConfigLoader` | ✅ Ready |
| `FileConfigSource` | wrknv | wrknv/wenv/config.py:65 | `foundation.config.FileConfigLoader` | Profile management |
| `EnvironmentConfigSource` | wrknv | wrknv/wenv/config.py:218 | `foundation.config.EnvConfigLoader` | ✅ Ready |
| `load_config()` | supsrc | supsrc/config/loader.py:174 | `foundation.config.FileConfigLoader` | Duration parsing |
| `_parse_duration()` | supsrc | supsrc/config/loader.py:58 | **GAP** - Add utility | ❌ Missing |

### Migration Example

```python
# OLD (wrknv)
from wrknv.wenv.config import FileConfigSource
source = FileConfigSource("config.toml")
config = source.load()

# NEW
from provide.foundation.config import FileConfigLoader
loader = FileConfigLoader("config.toml")
config = await loader.load(ConfigClass)

# OLD (supsrc)
from supsrc.config.loader import load_config
config = load_config(Path("supsrc.toml"))

# NEW
from provide.foundation.config import FileConfigLoader
loader = FileConfigLoader("supsrc.toml")
config = await loader.load(SupsrcConfig)
```

### Required Additions to Foundation

```python
# provide.foundation.config.utils (NEW FILE)
from datetime import timedelta

def parse_duration(duration_str: str) -> timedelta:
    """Parse duration string like '5m', '1h30m', '30s' to timedelta."""
    pass

def parse_size(size_str: str) -> int:
    """Parse size string like '10MB', '1GB' to bytes."""
    pass
```

## Implementation Roadmap

### Phase 1: Foundation Enhancements (Week 1-2)

- [ ] Add `provide.foundation.utils.file` module with atomic operations
- [ ] Add platform utility functions to `provide.foundation.platform.utils`
- [ ] Add tool-specific error types to `provide.foundation.errors`
- [ ] Add duration/size parsing to `provide.foundation.config.utils`
- [ ] Write comprehensive tests for new modules
- [ ] Update documentation

### Phase 2: Repository Migration (Week 3-4)

#### pyvider
- [ ] Replace `_run_command()` with `foundation.process.run_command()`
- [ ] Replace `terraform_arch()` and `terraform_os()` with foundation platform functions
- [ ] Update imports and tests

#### wrknv
- [ ] Replace platform detection with `foundation.platform`
- [ ] Migrate error classes to inherit from foundation errors
- [ ] Replace config loading with foundation loaders
- [ ] Update tests

#### flavorpack
- [ ] Move atomic operations to foundation
- [ ] Replace subprocess utilities with foundation process
- [ ] Update imports and tests

#### garnish
- [ ] Update error classes to inherit from foundation
- [ ] Replace `handle_error()` with foundation error handlers
- [ ] Update tests

#### supsrc
- [ ] Replace config loading with foundation patterns
- [ ] Move duration parsing to foundation
- [ ] Update tests

### Phase 3: Testing & Validation (Week 5)

- [ ] Run full test suites for all affected repositories
- [ ] Verify backwards compatibility where needed
- [ ] Performance benchmarking (ensure no regressions)
- [ ] Update integration tests
- [ ] Documentation updates

### Phase 4: Deprecation & Enforcement (Week 6)

- [ ] Mark duplicate implementations as deprecated with warnings
- [ ] Add migration guide to each repository
- [ ] Update CI/CD to enforce foundation usage
- [ ] Create linting rules to prevent new duplications
- [ ] Archive or remove deprecated code (after grace period)

## Rationale for Consolidation

### Current Problems

1. **Maintenance Burden**
   - 8+ different implementations of subprocess execution
   - Platform detection code duplicated in 3+ repositories
   - Each bug must be fixed multiple times

2. **Feature Gaps**
   - Some repos have robust error handling, others don't
   - Inconsistent logging and telemetry
   - Missing functionality in some implementations

3. **Development Velocity**
   - Developers reimplementing common patterns
   - Time wasted on "which version should I use?"
   - Onboarding complexity for new team members

4. **Quality Issues**
   - Inconsistent error messages
   - Different behavior for same operations
   - Variable test coverage

5. **Security Risk**
   - Security updates must be applied to multiple codebases
   - Easy to miss critical updates in lesser-used repos

### Expected Benefits

- **Single Source of Truth**: One implementation to maintain
- **Consistent Behavior**: Same operations work the same everywhere
- **Better Features**: All repos benefit from improvements
- **Faster Development**: Focus on business logic, not utilities
- **Improved Quality**: Better test coverage, more robust implementations
- **Easier Onboarding**: One set of patterns to learn

### Success Metrics

| Metric | Current | Target | Impact |
|--------|---------|--------|--------|
| Lines of duplicate code | ~2,500 | 0 | -100% |
| Utility test coverage | 65% | 95% | +30% |
| Average build time | 4.5 min | 3.5 min | -22% |
| Developer onboarding | 2 weeks | 1 week | -50% |
| Bug fix propagation | 3-5 days | Same day | -80% |

## Tracking Checklist

### Foundation Enhancements
- [ ] utils.file module created
- [ ] platform.utils enhancements complete
- [ ] New error types added
- [ ] Config utilities added
- [ ] All new tests passing
- [ ] Documentation updated

### Repository Migrations
- [ ] pyvider migrated
- [ ] wrknv migrated
- [ ] flavorpack migrated
- [ ] garnish migrated
- [ ] supsrc migrated
- [ ] pyvider-components migrated
- [ ] tofusoup migrated
- [ ] All tests passing

### Quality Assurance
- [ ] Performance benchmarks completed
- [ ] Security audit passed
- [ ] Documentation review complete
- [ ] Migration guides published

### Enforcement
- [ ] CI/CD rules updated
- [ ] Linting rules created
- [ ] Deprecation warnings added
- [ ] Team training completed

## Notes

- All line numbers are approximate and may change as code evolves
- Priority should be given to the most commonly used utilities
- Backwards compatibility should be maintained where possible
- Each migration should be done as a separate PR for easier review

---

*Last Updated: 2025-09-02*
*Document Version: 1.0.0*