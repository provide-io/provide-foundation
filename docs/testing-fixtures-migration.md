# Testing Fixtures Migration Guide

## Overview
New reusable test fixtures have been added to `provide.foundation.testing` for use across the provide-io ecosystem.

## Integration Options

### Option 1: Direct Import in Tests (Simplest)
**When to use**: For new tests or when refactoring individual test files

```python
# In any test file
from provide.foundation.testing import (
    temp_directory,
    test_files_structure,
    mock_http_config,
    clean_event_loop,
)

def test_something(temp_directory):
    # Use the fixture directly
    (temp_directory / "test.txt").write_text("data")
```

### Option 2: Re-export via conftest.py (Recommended)
**When to use**: For project-wide adoption with minimal changes

Create or update `tests/conftest.py`:
```python
# Re-export foundation fixtures for pytest discovery
from provide.foundation.testing import (
    # File fixtures
    temp_directory,
    test_files_structure,
    temp_file,
    binary_file,
    nested_directory_structure,
    empty_directory,
    readonly_file,
    
    # Async fixtures
    clean_event_loop,
    async_timeout,
    mock_async_process,
    
    # Mock fixtures
    mock_http_config,
    mock_telemetry_config,
    mock_logger,
    mock_transport,
    mock_cache,
    
    # Network fixtures
    free_port,
    mock_server,
    httpx_mock_responses,
)

# Re-export for pytest to discover
__all__ = [
    "temp_directory",
    "test_files_structure",
    # ... etc
]
```

### Option 3: Wrapper Fixtures (Most Flexible)
**When to use**: When you need project-specific customization

```python
# In tests/conftest.py
import pytest
from provide.foundation.testing import test_files_structure as foundation_test_files

@pytest.fixture
def test_files(foundation_test_files):
    """Project-specific test files with additional setup."""
    temp_path, source = foundation_test_files
    
    # Add project-specific files
    (source / "config.yaml").write_text("project: test")
    (source / "data.json").write_text('{"key": "value"}')
    
    return temp_path, source
```

## Migration Targets

### provide-foundation Tests to Update

#### High Priority (Heavy tempfile usage):
1. **tests/archive/** - All test files currently duplicate `test_files` fixture
   - `test_tar.py`, `test_gzip.py`, `test_zip.py`, `test_bzip2.py`
   - Replace local `test_files` fixtures with `test_files_structure`

2. **tests/file/** - Many duplicate temp directory patterns
   - `test_atomic.py`, `test_safe.py`, `test_directory.py`
   - Use `temp_directory` and `temp_file` fixtures

3. **tests/process/** - Async process mocking
   - Use `mock_async_process` and `clean_event_loop`

#### Medium Priority:
- **tests/transport/** - Replace local `http_config` fixtures
- **tests/config/** - Use `mock_config_source`
- **tests/streams/** - Use file fixtures

### flavorpack Tests to Update

#### High Priority (129 tempfile usages):
1. **tests/packaging/python/** - Heavy temp directory usage
   - Would benefit from `temp_directory` and `test_files_structure`

2. **tests/format_2025/** - Platform testing
   - Could use `mock_subprocess` and file fixtures

## Implementation Steps

### Step 1: Update provide-foundation tests/conftest.py
```python
# Add to existing tests/conftest.py
from provide.foundation.testing import (
    temp_directory,
    test_files_structure,
    temp_file,
    # ... other fixtures
)

# Keep existing fixtures, add new ones to __all__
__all__.extend([
    "temp_directory",
    "test_files_structure",
    "temp_file",
    # ...
])
```

### Step 2: Gradual Migration
Replace duplicated fixtures test-by-test:

```python
# Before (in test_tar.py)
@pytest.fixture
def test_files(self):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        source = temp_path / "source"
        source.mkdir()
        # ... setup
        yield temp_path, source

# After
# Just use the imported fixture directly
def test_create_tar_archive(self, tar_archive, test_files_structure):
    temp_path, source = test_files_structure
    # ... rest of test
```

### Step 3: Create flavorpack/tests/conftest.py
```python
"""
Flavorpack test configuration and fixtures.
"""
import pytest

# Import foundation testing utilities
from provide.foundation.testing import (
    temp_directory,
    test_files_structure,
    mock_subprocess,
    # ... others as needed
)

# Re-export for pytest
__all__ = [
    "temp_directory",
    "test_files_structure",
    "mock_subprocess",
]

# Add flavorpack-specific fixtures here
@pytest.fixture
def flavor_config():
    """Flavorpack-specific test configuration."""
    return {
        "format": "PSPF/2025",
        "version": "1.0.0",
    }
```

## Benefits of Migration

1. **DRY Principle**: Eliminate 100+ duplicate fixture definitions
2. **Consistency**: Same fixtures across all provide-io projects
3. **Maintenance**: Fix bugs in one place, benefit everywhere
4. **Performance**: Optimized fixtures with proper cleanup
5. **Features**: Get new fixture features automatically

## Quick Reference

### File Fixtures
- `temp_directory` - Empty temp directory
- `test_files_structure` - Standard file tree with content
- `temp_file` - Factory for temp files
- `binary_file` - Binary test file
- `nested_directory_structure` - Deep directory tree
- `readonly_file` - Read-only file for permission testing

### Async Fixtures
- `clean_event_loop` - Ensures clean event loop
- `mock_async_process` - Mock subprocess for async tests
- `async_timeout` - Timeout wrapper for async ops

### Mock Fixtures
- `mock_http_config` - Standard HTTP configuration
- `mock_logger` - Logger with captured calls
- `mock_transport` - Network transport mock
- `mock_cache` - Cache with test data tracking

### Network Fixtures
- `free_port` - Get available port
- `mock_server` - Simple HTTP server
- `tcp_client_server` - TCP socket pair

## Example Migration PR

```markdown
## PR: Migrate to foundation.testing fixtures

### Changes
- Added tests/conftest.py to re-export foundation fixtures
- Replaced 15 duplicate `test_files` fixtures with `test_files_structure`
- Replaced 8 tempfile.TemporaryDirectory uses with `temp_directory`
- Removed 200+ lines of duplicate fixture code

### Testing
- All existing tests pass
- No functional changes to tests
- Faster test execution due to optimized fixtures
```