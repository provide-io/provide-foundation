# provide-foundation Repository Replacement Checklist

## Overview
This document tracks the migration of all provide-io repositories to use `provide.foundation` as their core utility library, eliminating ~2,500 lines of duplicate code.

## Phase 1: Foundation Enhancements ✅ 
Adding missing functionality to provide-foundation before migration.

### 1.1 File Operations Module ✅
- [x] Create `provide.foundation.utils.file` module
- [x] Implement `atomic_write()` - Write files atomically with temp file
- [x] Implement `atomic_write_text()` - Text file atomic write  
- [x] Implement `atomic_replace()` - Replace existing file atomically
- [x] Implement `safe_unlink()` - Safe file deletion
- [x] Implement `ensure_directory()` - Ensure dir exists with permissions
- [x] Implement `read_file_safely()` - Safe file reading with defaults
- [x] Implement `read_text_safely()` - Safe text file reading

### 1.2 Platform Utilities Module ⏳
- [ ] Create `provide.foundation.platform.utils` module
- [ ] Add `is_supported_platform()` - Check platform/arch support
- [ ] Add `get_executable_extension()` - Get .exe for Windows, empty otherwise
- [ ] Add `get_archive_extension()` - Get platform-appropriate archive ext
- [ ] Add `get_tool_platform_mapping()` - Tool-specific platform mappings

### 1.3 Error Classes Enhancement ⏳
- [ ] Add `ToolError` base class to `provide.foundation.errors`
- [ ] Add `ToolNotFoundError` - When required tool is not found
- [ ] Add `PackageError` - Base for package management errors
- [ ] Add `DependencyError` - Missing or incompatible dependencies
- [ ] Add `BuildError` - Build process failures

### 1.4 Configuration Utilities ⏳
- [ ] Create `provide.foundation.config.utils` module
- [ ] Add `parse_duration()` - Parse duration strings like '5m', '1h30m'
- [ ] Add `parse_size()` - Parse size strings like '10MB', '1GB'
- [ ] Add `merge_configs()` - Deep merge configuration dictionaries
- [ ] Add `validate_config()` - Schema-based config validation

### 1.5 Testing Enhancements ⏳
- [ ] Write comprehensive tests for new file operations
- [ ] Write tests for platform utilities
- [ ] Write tests for new error classes
- [ ] Write tests for config utilities
- [ ] Ensure >95% coverage on new modules

## Phase 2: Repository Migrations ⏳

### 2.1 pyvider Migration
**Status**: Not Started
**Dependencies**: Uses internal utilities that need replacement

Replacements needed:
- [ ] Replace `pyvider.cli.utils._run_command()` → `foundation.process.run_command()`
- [ ] Replace `pyvider.cli.context.terraform_arch()` → `foundation.platform.get_arch_name()`
- [ ] Replace `pyvider.cli.context.terraform_os()` → `foundation.platform.get_os_name()`
- [ ] Update all imports and tests
- [ ] Remove deprecated utility modules

### 2.2 wrknv Migration  
**Status**: Not Started
**Dependencies**: Heavy platform detection and config usage

Replacements needed:
- [ ] Replace `wrknv.wenv.operations.platform` → `foundation.platform`
- [ ] Replace `wrknv.wenv.exceptions` → inherit from `foundation.errors`
- [ ] Replace `wrknv.wenv.config` → `foundation.config`
- [ ] Update environment script generation
- [ ] Update all tests

### 2.3 flavorpack Migration
**Status**: Not Started  
**Dependencies**: Atomic file operations, subprocess utilities

Replacements needed:
- [ ] Move `flavor.utils.atomic` → use `foundation.utils.file`
- [ ] Replace `flavor.utils.subprocess` → `foundation.process`
- [ ] Update packaging orchestrator
- [ ] Update all imports and tests
- [ ] Remove deprecated modules

### 2.4 garnish Migration
**Status**: Not Started
**Dependencies**: Error handling, potential logging improvements

Replacements needed:
- [ ] Update `garnish.errors` → inherit from `foundation.errors`
- [ ] Replace `handle_error()` → use foundation error handlers
- [ ] Ensure consistent logging with `foundation.logger`
- [ ] Update all tests

### 2.5 pyvider-rpcplugin Migration
**Status**: Partially Complete (tests already use foundation)
**Dependencies**: Already using foundation in tests

Replacements needed:
- [ ] Migrate main code to use `foundation.errors`
- [ ] Use `foundation.logger` throughout
- [ ] Remove any duplicate utilities
- [ ] Ensure consistency between tests and main code

### 2.6 pyvider-components Migration
**Status**: Not Started
**Dependencies**: Common utilities

Replacements needed:
- [ ] Use `foundation.errors` for all error classes
- [ ] Use `foundation.logger` for logging
- [ ] Replace any duplicate utilities
- [ ] Update all tests

### 2.7 supsrc Migration
**Status**: Not Started
**Dependencies**: Config loading, duration parsing

Replacements needed:
- [ ] Replace `supsrc.config.loader` → `foundation.config`
- [ ] Move `_parse_duration()` → use `foundation.config.utils`
- [ ] Update all imports and tests
- [ ] Remove deprecated modules

### 2.8 tofusoup Migration
**Status**: Not Started
**Dependencies**: Testing utilities

Replacements needed:
- [ ] Use `foundation.process` for subprocess operations
- [ ] Use `foundation.errors` for error handling
- [ ] Update logging to use `foundation.logger`
- [ ] Update all tests

## Phase 3: Validation & Testing ⏳

### 3.1 Integration Testing
- [ ] Run full test suite for each migrated repository
- [ ] Verify no functionality regression
- [ ] Performance benchmarking (ensure no slowdowns)
- [ ] Cross-repository integration tests

### 3.2 Documentation Updates
- [ ] Update README files for each repository
- [ ] Document foundation dependency
- [ ] Create migration guide for contributors
- [ ] Update API documentation

### 3.3 CI/CD Updates
- [ ] Update GitHub Actions workflows
- [ ] Add foundation as explicit dependency
- [ ] Ensure proper testing order
- [ ] Add linting rules to prevent reintroduction of duplicates

## Phase 4: Cleanup & Enforcement ⏳

### 4.1 Code Removal
- [ ] Remove all deprecated utility modules
- [ ] Delete duplicate implementations
- [ ] Clean up unused imports
- [ ] Archive old code if needed

### 4.2 Dependency Management
- [ ] Update all pyproject.toml files
- [ ] Pin foundation version appropriately
- [ ] Update lock files
- [ ] Verify dependency trees

### 4.3 Quality Assurance
- [ ] Code review all changes
- [ ] Security audit
- [ ] Performance validation
- [ ] Documentation review

## Success Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Lines of duplicate code | ~2,500 | 0 | ⏳ In Progress |
| Test coverage (foundation) | 90% | 95% | ⏳ In Progress |
| Repositories migrated | 0/8 | 8/8 | ⏳ Not Started |
| CI/CD pipelines passing | TBD | 100% | ⏳ Not Started |

## Notes

- All changes must maintain Python 3.11+ compatibility
- Use modern type hints (native types with | operator)
- No backward compatibility or migration code needed
- All imports must be absolute (no relative imports)
- Use `provide.foundation.logger` exclusively (never structlog directly)

## Related Documents

- `CONSOLIDATION_MATRIX.md` - Detailed function-level mapping
- `DEVELOPMENT.md` - Development guidelines
- `CLAUDE.md` - AI assistance guidelines

---

*Last Updated: 2025-09-03*
*Document Version: 1.0.0*