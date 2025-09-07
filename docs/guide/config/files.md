# Configuration Files

File-based configuration management for provide.foundation applications.

## Overview

Configuration files provide persistent, version-controlled configuration that can be shared across environments and teams. This section covers:

- **File Formats** - Supported configuration file formats and their usage
- **Loading & Profiles** - Loading strategies and profile-based configuration
- **Advanced Features** - Schema validation, hot reload, and advanced patterns

## Configuration File Topics

### [File Formats](files-formats.md)

Supported configuration file formats:
- YAML configuration files
- JSON configuration format  
- TOML configuration files
- INI/ConfigParser files
- Python configuration files
- Format comparison and recommendations

### [Loading & Profiles](files-loading.md)

Configuration loading strategies:
- Basic configuration loading
- Profile-based configuration
- Multi-file configuration
- Environment-specific file selection
- Merge and override strategies

### [Advanced Features](files-advanced.md)

Advanced file-based configuration:
- Configuration schema and validation
- Hot reload and file watching
- Configuration templates and variables
- Integration with other configuration sources
- Performance optimization

## Quick Reference

| Topic | Focus | Complexity |
|-------|-------|------------|
| [Formats](files-formats.md) | File format options | Basic |
| [Loading](files-loading.md) | Loading strategies | Intermediate |
| [Advanced](files-advanced.md) | Schema, validation, hot reload | Advanced |

## Related Documentation

- [Environment Variables](environment.md) - Environment-based configuration
- [Runtime Configuration](runtime.md) - Dynamic configuration management
- [Best Practices](best-practices.md) - Configuration best practices
- [Configuration Reference](reference.md) - Complete configuration options