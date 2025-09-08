# Testing Fixtures Integration Recommendations

## Executive Summary
New reusable test fixtures have been added to `provide.foundation.testing`. Both provide-foundation and flavorpack can benefit from using these fixtures to eliminate code duplication and improve test consistency.

## Current State

### provide-foundation
- **55 test files** with duplicate `test_files` fixtures
- **20+ files** using `tempfile` directly
- Fixtures now available via `tests/conftest.py`

### flavorpack
- **129 uses** of `tempfile`/`TemporaryDirectory`
- No central `conftest.py` yet
- Each test file manages its own fixtures

## Recommended Approach

### 1. **Use conftest.py Re-export Method** (Recommended)

**Why**: 
- Minimal code changes required
- Pytest automatically discovers fixtures
- Easy to add project-specific fixtures
- Can be done incrementally

**Implementation**:
1. For provide-foundation: ✅ Already done - `tests/conftest.py` updated
2. For flavorpack: Create `tests/conftest.py` using the example provided

### 2. **Migration Strategy**

#### Phase 1: Quick Wins (1-2 hours)
Update tests that have exact duplicate fixtures:

**provide-foundation targets**:
- `tests/archive/*.py` - Replace `test_files` fixtures (8 files)
- `tests/file/test_atomic.py` - Replace temp directory patterns
- `tests/transport/test_http_transport.py` - Use `mock_http_config`

**flavorpack targets**:
- `tests/packaging/python/*.py` - Heavy tempfile usage
- Create `tests/conftest.py` from example

#### Phase 2: Gradual Migration (ongoing)
- As tests are modified for other reasons, update to use new fixtures
- New tests should always use the foundation fixtures

#### Phase 3: Async Test Fixes (when issues arise)
- Apply `clean_event_loop` to problematic async tests
- Use `mock_async_process` for subprocess testing

## Specific Recommendations

### For provide-foundation

1. **Immediate Actions**:
   ```bash
   # Run serial tests separately to avoid freezing
   pytest -m "not serial" -n 4  # Parallel tests
   pytest -m serial -n 0         # Serial tests
   ```

2. **Test Organization**:
   - Use new markers: `@pytest.mark.archive`, `@pytest.mark.process`
   - Run without skip spam: `pytest -rFE`

3. **Fixture Migration Example**:
   ```python
   # OLD (in test file)
   @pytest.fixture
   def test_files(self):
       with tempfile.TemporaryDirectory() as temp_dir:
           # ... setup
   
   # NEW (just use from conftest)
   def test_something(self, test_files_structure):
       temp_path, source = test_files_structure
   ```

### For flavorpack

1. **Create `tests/conftest.py`**:
   ```bash
   cp docs/flavorpack-conftest-example.py ../flavorpack/tests/conftest.py
   ```

2. **Update High-Value Tests First**:
   - `tests/packaging/python/test_wheel_builder.py` - Uses many temp dirs
   - `tests/packaging/python/test_uv_manager.py` - Could use mock fixtures
   - `tests/format_2025/*.py` - Platform testing files

3. **Add Project-Specific Fixtures**:
   ```python
   # In flavorpack's conftest.py
   @pytest.fixture
   def sample_flavor(temp_directory):
       """Create a sample flavor for testing."""
       flavor_dir = temp_directory / "test_flavor"
       flavor_dir.mkdir()
       # ... setup
       return flavor_dir
   ```

## Benefits of This Approach

1. **Immediate Benefits**:
   - No skip spam in test output
   - Reusable fixtures available now
   - Better async test stability

2. **Long-term Benefits**:
   - Less test code to maintain
   - Consistent test patterns across projects
   - Automatic fixture improvements from foundation

3. **Ecosystem Benefits**:
   - Any provide-io project can use these fixtures
   - Standardized testing patterns
   - Shared best practices

## Quick Command Reference

```bash
# Run tests with new configuration
pytest -rFE                    # No skip spam
pytest -m "fast and unit"      # Fast unit tests only
pytest -m serial -n 0          # Serial async tests
pytest tests/archive/          # Specific module

# Debug hanging tests
pytest --timeout=30            # 30s timeout per test
pytest -x --tb=short          # Stop on first failure

# Performance testing
pytest -n auto -m "not slow"  # Parallel, skip slow tests
```

## Migration Checklist

- [x] Create foundation testing fixtures
- [x] Update foundation's conftest.py
- [x] Add test markers to pyproject.toml
- [x] Mark problematic async tests as serial
- [ ] Create flavorpack's conftest.py
- [ ] Migrate duplicate fixtures in foundation
- [ ] Migrate flavorpack's tempfile usage
- [ ] Document in both project READMEs

## Next Steps

1. **For provide-foundation**: Start migrating `tests/archive/*.py` fixtures
2. **For flavorpack**: Copy the example conftest.py and test it
3. **Monitor**: Watch for event loop issues in CI, apply serial markers as needed

## Questions?

The new fixtures are documented in:
- API: `src/provide/foundation/testing/*.py`
- Guide: `docs/testing-fixtures-migration.md`
- Example: `docs/flavorpack-conftest-example.py`