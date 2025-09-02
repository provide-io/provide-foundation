# CLI Implementation Status Checklist for Provide-io Ecosystem

## Active CLI Tools Analysis

| Tool | Has Click | Has Custom Context | Has Logging Decorator | Has Help System | Has Version Flag | Has Entry Point | Has Env Vars | Has Config File | Has JSON Output | Has Error Handling | **Needs** |
|------|-----------|-------------------|----------------------|-----------------|------------------|-----------------|---------------|-----------------|-----------------|-------------------|-----------|
| **wrknv** | ✅ | ❌ (uses dict) | ❌ | ✅ | ❌ | ✅ `wrknv.wenv.cli:entry_point` | ✅ | ✅ WorkenvConfig | ❌ | ✅ try/except | • Custom context class<br>• Logging decorator pattern<br>• Version flag<br>• JSON output option |
| **supsrc** | ✅ | ❌ (uses dict) | ✅ `@logging_options` | ✅ | ✅ `--version` | ✅ `supsrc.cli.main:cli` | ✅ SUPSRC_* | ✅ | ✅ `--json-logs` | ✅ | • Custom context class<br>• Standardize error codes |
| **pyvider** | ✅ | ✅ PyviderContext | ❌ | ✅ | ❌ | ✅ `pyvider.cli.__main__:main` | ❌ | ✅ | ❌ | ✅ | • Logging decorator<br>• Version flag<br>• Env var support<br>• JSON output<br>• Structured logging |
| **garnish** | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ `garnish.cli:main` | ❌ | ❌ | ❌ | ❌ | • Custom context<br>• Logging decorator<br>• Version flag<br>• Config support<br>• Error handling |
| **flavor** | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ `flavor.cli:main` | ❌ | ❌ | ❌ | ❌ | • Custom context<br>• Logging decorator<br>• Version flag<br>• Config support<br>• Error handling |
| **soup** (tofusoup) | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ `tofusoup.cli:entry_point` | ❌ | ❌ | ❌ | ❌ | • Custom context<br>• Logging decorator<br>• Version flag<br>• Config support<br>• Error handling |
| **terraform-provider-pyvider** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ `pyvider.cli:main` | ❌ | ❌ | ✅ (RPC) | ✅ | • Click integration<br>• Proper CLI structure<br>• Help system |

## Feature Implementation Details

### 1. **Click Framework**
| Tool | Implementation | Needs |
|------|---------------|-------|
| wrknv | `@click.group()` with subcommands | - |
| supsrc | `@click.group()` with command modules | - |
| pyvider | `@click.group()` with assembled commands | - |
| Others | Basic `@click.command()` | Full command group structure |

### 2. **Custom Context Pattern**
| Tool | Current | Target Implementation |
|------|---------|----------------------|
| wrknv | `ctx.obj = {}` | `ctx.obj = WrknvContext()` with typed attributes |
| supsrc | `ctx.ensure_object(dict)` | `ctx.obj = SupsrcContext()` with lazy loading |
| pyvider | ✅ `PyviderContext` | Add more state management |
| Others | None | Create context classes with standard attributes |

### 3. **Logging Configuration**
| Tool | Current | Target Pattern |
|------|---------|---------------|
| wrknv | Direct visual module | Add `@logging_options` decorator |
| supsrc | ✅ `@logging_options` decorator | Keep as reference implementation |
| pyvider | Basic `click.secho()` | Add structlog + decorator |
| Others | None | Implement supsrc pattern |

### 4. **Standard Options Needed**
```python
# Every CLI should have:
@click.option('--version', '-V', is_flag=True)
@click.option('--log-level', '-l', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']))
@click.option('--log-file', type=click.Path())
@click.option('--json', '--json-output', is_flag=True)
@click.option('--config', '-c', type=click.Path(exists=True))
@click.option('--profile', '-p', help='Configuration profile to use')
```

### 5. **Environment Variable Support**
| Tool | Pattern | Standard Format |
|------|---------|----------------|
| wrknv | Manual checking | `WRKNV_*` prefix |
| supsrc | ✅ `envvar="SUPSRC_*"` | Reference pattern |
| pyvider | None | Add `PYVIDER_*` |
| Others | None | Add `TOOLNAME_*` |

### 6. **Configuration Precedence**
**Target Standard** (highest to lowest priority):
1. CLI arguments
2. Environment variables
3. Config file
4. Defaults

| Tool | Has Precedence | Implementation |
|------|---------------|----------------|
| supsrc | ✅ Full | Reference implementation |
| wrknv | Partial | Add env vars to chain |
| Others | ❌ | Implement full chain |

### 7. **Error Handling Pattern**
```python
# Standard error handling needed:
try:
    # command logic
except SpecificError as e:
    ctx.obj.logger.error(f"Operation failed: {e}")
    raise click.ClickException(str(e))
except Exception as e:
    if ctx.obj.debug:
        raise
    click.secho(f"Error: {e}", fg='red', err=True)
    sys.exit(1)
```

### 8. **Output Formatting**
| Tool | Text | JSON | Structured | Needs |
|------|------|------|------------|-------|
| wrknv | Rich/emoji | ❌ | ❌ | JSON option |
| supsrc | Structlog | ✅ | ✅ | - |
| pyvider | click.secho | ❌ | ❌ | JSON + structured |
| Others | Basic | ❌ | ❌ | All formatting options |

## Standardization Targets

### Core Module Structure
```
package/
├── cli/
│   ├── __init__.py      # Assemble CLI
│   ├── __main__.py      # Entry point
│   ├── context.py       # Custom context class
│   ├── decorators.py    # @logging_options, etc.
│   ├── main.py          # Main CLI group
│   └── commands/        # Subcommand modules
│       ├── config.py
│       ├── ...
```

### Required Base Context Class
```python
@dataclass
class BaseCliContext:
    """Standard context all CLIs should extend"""
    log_level: str = "INFO"
    log_file: Path | None = None
    json_output: bool = False
    config_file: Path | None = None
    profile: str = "default"
    debug: bool = False
    _logger: Any = field(init=False, default=None)
    _config: Any = field(init=False, default=None)
```

### Missing Critical Features by Tool

**wrknv**:
- [ ] Custom context class
- [ ] Logging decorator
- [ ] Version flag
- [ ] JSON output
- [ ] Env var documentation

**supsrc**: ✅ Most complete, use as reference

**pyvider**:
- [ ] Logging configuration
- [ ] Environment variables
- [ ] JSON output formatting
- [ ] Version flag
- [ ] Config file precedence

**garnish/flavor/soup**:
- [ ] Everything except basic Click usage
- [ ] Need complete rewrite using supsrc as template

**terraform-provider-pyvider**:
- [ ] Needs separation from main pyvider CLI
- [ ] RPC-specific command structure

## Implementation Priority

### Phase 1: Standardize Core Tools
1. **wrknv** - Add context class and logging decorator
2. **pyvider** - Add logging and environment variables
3. **supsrc** - Convert dict to context class (minor change)

### Phase 2: Update Secondary Tools
4. **garnish** - Full CLI rewrite
5. **flavor** - Full CLI rewrite
6. **tofusoup** - Full CLI rewrite

### Phase 3: Special Cases
7. **terraform-provider-pyvider** - Separate RPC handler from CLI

## Standard Decorator Library

Create `provide.foundation.cli` module with:
```python
from provide.foundation.cli import (
    logging_options,      # Standard logging decorator
    config_options,       # Standard config decorator
    output_options,       # JSON/format decorator
    BaseCliContext,       # Base context class
    standard_error_handler,  # Error handling decorator
)
```

## provide.foundation Updates (Completed)

### Console Output Standardization ✅
- `pout()` - Output to stdout with JSON mode support
- `perr()` - Output to stderr with JSON mode support  
- `plog` - Alias for foundation.logger

### Command Registration with Dot Notation ✅
- Commands use dot notation for hierarchy: `@register_command("db.migrate")`
- Auto-creates parent groups as needed
- Groups can be explicit: `@register_command("db", group=True)`
- Supports multi-level nesting: `container.volumes.backup`

### Test Infrastructure Reorganization ✅
- Tests organized by feature in subdirectories
- Test files use `test_<feature>_` prefix convention
- Created infrastructure directories:
  - `tests/mocks/` - Reusable mock objects
  - `tests/fixtures/` - Organized pytest fixtures
  - `tests/data/` - Test data files
  - `tests/helpers/` - Test utilities

## Testing Requirements

Each CLI tool needs:
- [ ] Unit tests for context class
- [ ] Integration tests for command flow
- [ ] Mock tests for external dependencies
- [ ] Error handling tests
- [ ] Configuration precedence tests
- [ ] JSON output format tests

## Documentation Requirements

Each CLI needs:
- [ ] README with usage examples
- [ ] Environment variable documentation
- [ ] Configuration file schema
- [ ] Command reference (auto-generated from Click)
- [ ] Error code reference
- [ ] JSON output schema documentation