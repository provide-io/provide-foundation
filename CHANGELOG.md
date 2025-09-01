# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Platform Detection Module** (`foundation.platform`)
  - Cross-platform OS and architecture detection
  - System information gathering (CPU, memory, disk)
  - Normalized platform strings for consistent behavior
  
- **Process Execution Module** (`foundation.process`)
  - Safe subprocess execution with structured logging
  - Both synchronous and asynchronous APIs
  - Timeout support and comprehensive error handling
  - Output streaming capabilities
  
- **Console Output Functions** (`foundation.console`)
  - `pout()` for stdout output
  - `perr()` for stderr output
  - `plog` alias for the logger
  - JSON output mode support
  - Testing utilities with output capture
  
- **Enhanced CLI Framework**
  - Nested command support with dot notation
  - Command groups and hierarchies
  - Improved command registration decorators
  
- **Registry Pattern** (`foundation.Registry`)
  - Thread-safe multi-dimensional object storage
  - Support for aliases and metadata
  - Iteration and querying capabilities
  
- **Error Handling Improvements**
  - `AlreadyExistsError` for duplicate registrations
  - `ConfigurationError` for config issues
  - `PlatformError` for platform detection failures
  - `ProcessError` and `TimeoutError` for process execution

### Changed
- Logger is now also available as `plog` for consistency
- All test failures fixed (709 tests passing)
- Improved thread safety in Hub and Registry components
- Better error messages with structured context

### Fixed
- Registry now properly raises `AlreadyExistsError` instead of `ValueError`
- Config loader error handling improvements
- CLI argument ordering in nested commands
- Thread safety issues in concurrent operations
- Context validation for strict type checking

### Documentation
- Complete API documentation for all new modules
- Updated mkdocs configuration
- Cleaned up development/planning documents
- Comprehensive examples and best practices

## [0.1.0] - 2025-06-06

### Added
- Initial release of provide.foundation
- Feature-rich logging library with emoji support, structured logging, and Domain, Action, Status (DAS) patterns
- Comprehensive test suite and documentation