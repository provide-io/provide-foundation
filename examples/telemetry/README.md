# Telemetry Examples

Core logging and telemetry features of provide-foundation.

## Examples

### 01_basic_logging.py
The simplest possible Foundation setup - zero configuration logging that works out of the box.

**Features:**
- Automatic telemetry initialization
- Structured key-value logging
- Visual emoji enhancement

### 02_structured_logging.py  
Complete telemetry setup with full Foundation features enabled.

**Features:**
- Custom telemetry configuration
- Service naming
- Context binding
- Performance metrics

### 03_named_loggers.py
Component-specific loggers for different parts of your application.

**Features:**
- Named logger creation
- Module-specific logging
- Hierarchical logger organization

### 04_das_pattern.py
Domain-Action-Status structured logging pattern.

**Features:**
- Semantic event naming
- Domain-specific vocabularies
- Status-based visual indicators
- Event enrichment with emojis

### 05_exception_handling.py
Comprehensive exception logging with automatic traceback capture.

**Features:**
- Automatic traceback inclusion
- Exception context preservation
- Error categorization

### 06_trace_logging.py
Ultra-verbose TRACE level logging for deep diagnostics.

**Features:**
- TRACE level configuration
- Verbose diagnostic output
- Development debugging patterns

### 07_module_filtering.py
Fine-grained control over log levels per module.

**Features:**
- Module-specific log levels
- Runtime level adjustments
- Filtering configuration

## Running Order

1. Start with `01_basic_logging.py` for the simplest introduction
2. Move to `02_structured_logging.py` for complete setup
3. Explore `04_das_pattern.py` for semantic logging patterns
4. Use `05_exception_handling.py` for error handling patterns
5. Try `03_named_loggers.py` and `07_module_filtering.py` for organization