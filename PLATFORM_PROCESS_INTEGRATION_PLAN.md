# Platform & Process Utilities Integration Plan

## Current Status

### Test Results
- **Total Tests**: 649
- **Passing**: 642
- **Failing**: 7

### Test Failures Analysis
1. **Registry Tests** (2 failures)
   - `tests/registry/test_registry_core.py::TestRegistry::test_registry_prevents_duplicate_names`
   - `tests/hub/test_hub_registry.py::TestRegistry::test_registry_prevents_duplicate_names`
   - Issue: Tests expect `ValueError` but now getting `AlreadyExistsError`

2. **CLI/Hub Tests** (1 failure)
   - `tests/hub/test_hub_dot_notation_commands.py::TestDotNotationIntegration::test_mixed_explicit_and_auto_groups`
   - Issue: Command argument parsing problem

3. **Semantic Layer Test** (1 failure)
   - `tests/semantic_layers/test_semantic_layers_core.py::TestSetupWithLayers::test_env_var_parsing_for_layers`
   - Issue: Emoji formatting expectation mismatch

## Missing Foundation Utilities

Based on analysis of flavorpack and other provide-io projects, foundation is missing critical utilities that are being re-implemented across projects:

### 1. Platform Detection (`foundation.platform`)
- [ ] OS detection and normalization
- [ ] Architecture detection
- [ ] Platform string generation
- [ ] OS version detection
- [ ] CPU type information

### 2. Process Management (`foundation.process`)
- [ ] Unified subprocess execution
- [ ] Structured logging integration
- [ ] Error handling with rich context
- [ ] Timeout support
- [ ] Environment variable management
- [ ] Output capture options
- [ ] Async process execution

### 3. System Information (`foundation.system`)
- [ ] Memory information
- [ ] Disk usage
- [ ] Network interfaces
- [ ] Process information

## Implementation Checklist

### Phase 1: Fix Existing Test Failures

#### Registry Test Fixes
- [ ] Update `tests/registry/test_registry_core.py` to expect `AlreadyExistsError`
- [ ] Update `tests/hub/test_hub_registry.py` to expect `AlreadyExistsError`

#### CLI Test Fixes
- [ ] Debug argument order issue in dot notation commands
- [ ] Fix command name extraction logic

#### Semantic Layer Test Fix
- [ ] Update emoji expectation in test

### Phase 2: Platform Module Implementation

#### Module Structure
```
src/provide/foundation/platform/
├── __init__.py
├── detection.py     # Core detection functions
├── info.py         # System information gathering
└── types.py        # Platform-related types
```

#### Core Functions
- [ ] `get_os_name() -> str` - Normalized OS name (darwin, linux, windows)
- [ ] `get_arch_name() -> str` - Normalized architecture (amd64, arm64, x86)
- [ ] `get_platform_string() -> str` - Combined platform string
- [ ] `get_os_version() -> str | None` - OS version information
- [ ] `get_cpu_type() -> str | None` - CPU type/family
- [ ] `normalize_platform_components(os: str, arch: str) -> tuple[str, str]`

#### Error Handling
- [ ] Add `PlatformError` to errors hierarchy
- [ ] Handle platform detection failures gracefully
- [ ] Log platform information at debug level

### Phase 3: Process Module Implementation

#### Module Structure
```
src/provide/foundation/process/
├── __init__.py
├── runner.py       # Core subprocess execution
├── async_runner.py # Async process execution
└── types.py        # Process-related types
```

#### Core Functions
- [ ] `run_command(cmd: list[str], **kwargs) -> CompletedProcess`
- [ ] `run_command_simple(cmd: list[str], **kwargs) -> str`
- [ ] `async_run_command(cmd: list[str], **kwargs) -> CompletedProcess`
- [ ] `stream_command(cmd: list[str], **kwargs) -> AsyncIterator[str]`

#### Features
- [ ] Structured logging with foundation.logger
- [ ] Error handling with `ProcessError`
- [ ] Timeout support with `TimeoutError`
- [ ] Environment variable management
- [ ] Working directory support
- [ ] Output capture (stdout/stderr)
- [ ] Real-time output streaming
- [ ] Command logging with emojis

#### Error Handling
- [ ] Add `ProcessError` to errors hierarchy
- [ ] Include command, exit code, stdout/stderr in error context
- [ ] Support retry logic with `@retry_on_error`

### Phase 4: Integration & Testing

#### Test Structure
```
tests/platform/
├── test_platform_detection.py
├── test_platform_info.py
└── test_platform_normalization.py

tests/process/
├── test_process_runner.py
├── test_process_async.py
├── test_process_streaming.py
└── test_process_errors.py
```

#### Test Coverage
- [ ] Platform detection on different OS/arch combinations
- [ ] Process execution success cases
- [ ] Process execution failure cases
- [ ] Timeout handling
- [ ] Environment variable passing
- [ ] Output capture modes
- [ ] Async execution
- [ ] Error context propagation

### Phase 5: Documentation & Examples

#### Documentation
- [ ] API documentation for platform module
- [ ] API documentation for process module
- [ ] Usage examples in docstrings
- [ ] Integration guide for other projects

#### Migration Guide
- [ ] How to migrate from custom subprocess code
- [ ] How to replace platform.system() calls
- [ ] Error handling best practices

## Example Usage

### Platform Detection
```python
from provide.foundation.platform import (
    get_platform_string,
    get_os_name,
    get_arch_name,
    get_cpu_type
)

# Get normalized platform info
platform = get_platform_string()  # "darwin_arm64"
os_name = get_os_name()          # "darwin"
arch = get_arch_name()            # "arm64"
cpu = get_cpu_type()              # "Apple M2"
```

### Process Execution
```python
from provide.foundation.process import run_command, ProcessError
from provide.foundation.errors.decorators import retry_on_error

# Simple command execution
try:
    result = run_command(
        ["git", "status"],
        cwd="/path/to/repo",
        timeout=30,
        capture_output=True
    )
    print(result.stdout)
except ProcessError as e:
    logger.error("Git command failed", **e.context)

# With retry logic
@retry_on_error(max_attempts=3, exceptions=(ProcessError,))
def deploy():
    return run_command(["./deploy.sh"], check=True)

# Async execution
async def run_tests():
    result = await async_run_command(
        ["pytest", "tests/"],
        capture_output=True
    )
    return result.returncode == 0
```

## Benefits

1. **Consistency**: Single source of truth for platform/process operations
2. **Logging**: All subprocess calls automatically logged with structure
3. **Error Handling**: Rich error context for debugging
4. **Cross-platform**: Normalized platform detection across OS
5. **Reusability**: No more duplicated subprocess code
6. **Testing**: Easier to mock and test process execution
7. **Async Support**: Modern async/await patterns supported

## Success Criteria

- [ ] All existing tests pass (649 tests)
- [ ] Platform detection works on Linux, macOS, Windows
- [ ] Process execution handles all common use cases
- [ ] Error messages include helpful context
- [ ] Logging output is structured and searchable
- [ ] Documentation is complete and helpful
- [ ] Other provide-io projects can adopt easily

## Timeline Estimate

- Phase 1 (Fix tests): 30 minutes
- Phase 2 (Platform module): 2 hours
- Phase 3 (Process module): 3 hours
- Phase 4 (Testing): 2 hours
- Phase 5 (Documentation): 1 hour

**Total**: ~8-9 hours of implementation