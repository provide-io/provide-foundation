# CLI Tool

Command-line interface development with argument handling and structured logging.

## Overview

This example demonstrates building a CLI tool using provide-foundation's CLI framework, including command registration, argument parsing, and proper output handling.

## Code Example

```python
#!/usr/bin/env python3
"""
CLI Tool Example

Demonstrates CLI command registration and argument handling.
"""

from provide.foundation import Context, logger, setup_telemetry
from provide.foundation.hub import register_command
from provide.foundation.console import pout, perr
from pathlib import Path


@register_command("greet")
def greet_command(name: str = "World", greeting: str = "Hello", count: int = 1):
    """Greet someone with a custom message.
    
    Args:
        name: Name of the person to greet
        greeting: Greeting message to use
        count: Number of times to repeat the greeting
    """
    logger.info("command_start", command="greet", name=name, count=count)
    
    for i in range(count):
        pout(f"{greeting}, {name}!")
        logger.debug("greeting_sent", iteration=i+1, name=name)
    
    logger.info("command_complete", command="greet", status="success")


@register_command("process-file")
def process_file_command(file_path: Path, output_dir: Path = Path("./output")):
    """Process a file and save results to output directory.
    
    Args:
        file_path: Path to the input file to process
        output_dir: Directory to save processed results
    """
    logger.info("file_processing_start", 
                input_file=str(file_path),
                output_dir=str(output_dir))
    
    try:
        # Validate input file exists
        if not file_path.exists():
            perr(f"❌ File not found: {file_path}")
            logger.error("file_not_found", path=str(file_path))
            return 1
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("output_directory_created", path=str(output_dir))
        
        # Simulate file processing
        content = file_path.read_text()
        processed_content = content.upper()  # Simple processing
        
        # Write output
        output_file = output_dir / f"processed_{file_path.name}"
        output_file.write_text(processed_content)
        
        pout(f"✅ File processed successfully: {output_file}")
        logger.info("file_processing_complete",
                   input_file=str(file_path),
                   output_file=str(output_file),
                   status="success")
        
        return 0
        
    except Exception as e:
        perr(f"❌ Processing failed: {e}")
        logger.exception("file_processing_failed",
                        input_file=str(file_path),
                        error=str(e))
        return 1


@register_command("status")
def status_command():
    """Show application status and configuration."""
    ctx = Context.from_env()
    
    pout("📊 Application Status")
    pout(f"Profile: {ctx.profile}")
    pout(f"Log Level: {ctx.log_level}")
    pout(f"Debug Mode: {ctx.debug}")
    pout(f"JSON Output: {ctx.json_output}")
    
    logger.info("status_displayed", 
                profile=ctx.profile,
                log_level=ctx.log_level,
                debug=ctx.debug)


def setup_cli():
    """Setup CLI application with telemetry."""
    ctx = Context.from_env()
    setup_telemetry()
    
    logger.info("cli_initialized", 
                profile=ctx.profile)


if __name__ == "__main__":
    setup_cli()
    
    # The CLI framework will automatically handle command dispatch
    # based on registered commands and command-line arguments
```

## Key Features Demonstrated

### Command Registration
- Decorator-based command registration with `@register_command`
- Automatic help generation from docstrings
- Type-annotated parameters with default values

### Argument Handling
- Automatic conversion of CLI arguments to Python types
- Support for `Path`, `str`, `int`, and other built-in types
- Default value handling and validation

### Output Management
- User-facing output with `pout()` for success messages
- Error output with `perr()` for error messages
- Structured logging for debugging and monitoring

### Error Handling
- Proper exception handling with logging
- Return codes for CLI conventions
- User-friendly error messages

## Running the CLI Tool

### Basic Commands

```bash
# Greet with defaults
python cli_tool.py greet

# Greet with custom parameters
python cli_tool.py greet --name "Alice" --greeting "Hi" --count 3

# Process a file
python cli_tool.py process-file --file-path input.txt --output-dir ./results

# Show status
python cli_tool.py status
```

### Help and Documentation

```bash
# Show all available commands
python cli_tool.py --help

# Show help for specific command
python cli_tool.py greet --help
```

## Expected Output

### Greet Command
```bash
$ python cli_tool.py greet --name "Alice" --count 2
Hello, Alice!
Hello, Alice!
```

### Process File Command
```bash
$ python cli_tool.py process-file --file-path sample.txt
✅ File processed successfully: ./output/processed_sample.txt
```

### Status Command
```bash
$ python cli_tool.py status
📊 Application Status
Profile: development
Log Level: INFO
Debug Mode: False
JSON Output: False
```

## Configuration

Configure the CLI tool through environment variables:

```bash
# CLI-specific settings
export FOUNDATION_LOG_LEVEL=DEBUG
export FOUNDATION_PROFILE=production
export FOUNDATION_SERVICE_NAME=my-cli-tool

# Enable JSON logging for structured output
export FOUNDATION_JSON_OUTPUT=true
```

## Advanced Usage

### Custom Context
```python
def setup_cli_with_custom_context():
    """Setup CLI with custom context configuration."""
    ctx = Context(
        profile="cli",
        log_level="INFO",
        service_name="advanced-cli-tool",
        debug=False
    )
    
    setup_telemetry(ctx.to_telemetry_config())
```

### Command Groups
```python
@register_command("db:migrate")
def db_migrate_command():
    """Run database migrations."""
    logger.info("migration_start", operation="db_migrate")
    # Migration logic here
    pout("✅ Database migration completed")

@register_command("db:seed")
def db_seed_command():
    """Seed database with initial data."""
    logger.info("seeding_start", operation="db_seed")
    # Seeding logic here
    pout("✅ Database seeding completed")
```

## Next Steps

- Explore [Web Service](web-service.md) for HTTP service patterns
- Learn about [Data Pipeline](data-pipeline.md) for data processing workflows
- Review [Basic Application](basic-app.md) for simpler application patterns