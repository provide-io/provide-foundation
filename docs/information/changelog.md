# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed
- Removed workenv/wrknv dependency - project now uses standard Python virtual environment setup
- Removed all references to `.wrknv` directories - now uses `.provide-foundation` for tool installations

### Changed
- Tools module now uses `.provide-foundation` directory instead of `.wrknv` for tool cache and installations
- Registry now uses `provide.foundation.tools` entry point group instead of `wrknv.tools`
- Simplified development setup to use standard `uv venv` and `.venv` directory

## [0.1.0-beta.2] - 2025-01-14

### Removed (Breaking Changes)
- **BREAKING**: Removed deprecated `setup_foundation()` function - use `get_hub().initialize_foundation(config)` instead
- **BREAKING**: Removed deprecated `setup_telemetry()` function - use `get_hub().initialize_foundation(config)` instead
- **BREAKING**: Removed deprecated `setup_logging()` function - Foundation now auto-initializes on first use
- **BREAKING**: Removed deprecated `emoji` and `emoji_hierarchy` parameters from `get_logger()` - replaced by event sets

### Fixed
- Fixed RecursionError in Foundation `__getattr__` method that caused infinite loops when importing CLI modules
- Fixed `provide.foundation.hub` module access through lazy loading
- Resolved security vulnerabilities identified by bandit scan (tarfile extraction, shell injection, SQL injection)

### Improved
- **Code Quality**: Comprehensive "dogfooding" - Foundation now uses its own utilities consistently throughout codebase
- **Security**: All high/medium severity security findings addressed
- **API Surface**: Simplified API by removing all deprecated functions and parameters
- **Documentation**: Updated example files to use modern Hub-based initialization

### Changed
- All setup functions now route through Hub-based initialization system
- Examples updated to demonstrate Hub-based configuration instead of deprecated setup functions

## [0.1.0-beta.1] - 2025-01-13

### Added
- Initial beta release of provide.foundation
- Structured logging with emoji-enhanced visual parsing
- CLI framework with command registration and comprehensive subcommands
- Configuration management system with environment variable support
- Cryptographic utilities (hash, signatures, certificates)
- File operations with atomic write support
- Console I/O with color support and proper output handling
- Platform detection and system utilities
- Process execution with streaming support
- Error handling with retry logic and error boundaries
- Registry pattern for component management
- OpenTelemetry integration for distributed tracing
- OpenObserve integration for log aggregation
- Rate limiting with token bucket algorithm
- Comprehensive example suite

### Improved
- **Code Quality**: Reduced cyclomatic complexity violations from 41 to 39 (C901)
- **Error Handling**: Improved exception chaining patterns (B904)
- **Type Safety**: Enhanced type annotations and resolved type errors
- **Test Coverage**: Increased from 79.84% to 82.50% (exceeding 80% target)
- **Import Organization**: Fixed all 45 import sorting issues (I001)
- **Code Organization**: Fixed all 22 unsorted __all__ declarations

### Fixed
- Complex function refactoring in CLI commands (query, send, generate)
- Type annotation errors in configuration parsers
- Missing imports for NoReturn, Callable, and other typing constructs
- Exception chaining in error handling
- Click decorator placement in CLI commands

### Added Tests
- Comprehensive config error handling tests (33 new tests, 100% coverage)
- CLI logs generate command tests (30 new tests, coverage improved from 18.48% to 61.96%)
- Config defaults tests (39 new tests, 100% coverage)

### Technical Improvements
- Moved from lambda factories to proper named functions in config defaults
- Enhanced type safety with proper cast() usage for string literals
- Improved function complexity through strategic helper function extraction
- Better separation of concerns in CLI command implementations

### Dependencies
- Python 3.11+ required
- Built on structlog, attrs, and modern Python typing
- Optional dependencies for CLI (click), crypto (cryptography), transport (httpx), and OpenTelemetry

### Documentation
- Complete API documentation
- Getting started guide
- Practical examples for all major features
- Environment variable configuration reference

---

**Note**: This is a pre-release version. APIs may change before 1.0.0.

---

[Return to Documentation Home](../index.md)
