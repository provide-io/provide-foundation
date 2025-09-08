#!/usr/bin/env python3

import os
import sys
import json

# Add the src directory to the path
sys.path.insert(0, '/Users/tim/code/gh/provide-io/provide-foundation/src')

# Set up testing environment
os.environ["CLICK_TESTING"] = "1"

print("Starting CLI debug test...")

try:
    import click
    from provide.foundation.context import Context
    from provide.foundation.cli.decorators import (
        flexible_options,
        output_options,
        pass_context,
    )
    from provide.foundation.cli.utils import (
        CliTestRunner,
        setup_cli_logging,
    )
    from provide.foundation.logger import get_logger
    from provide.foundation.testing import reset_foundation_setup_for_testing
    
    print("All imports successful")
    
    # Reset foundation state
    print("Resetting foundation state...")
    reset_foundation_setup_for_testing()
    print("Foundation reset successful")
    
    @click.command()
    @flexible_options
    @output_options
    @pass_context
    def test_cmd(ctx: Context, **kwargs) -> None:
        """Test command."""
        for key, value in kwargs.items():
            if value is not None:
                setattr(ctx, key, value)
        setup_cli_logging(ctx)
        
        logger = get_logger(__name__)
        logger.info("Test command executed")
        if ctx.json_output:
            click.echo(json.dumps({"status": "success"}))
        else:
            click.echo("Test successful")
    
    print("Created test command")
    
    runner = CliTestRunner()
    print("Created CLI test runner")
    
    print("Invoking CLI command...")
    result = runner.invoke(test_cmd, ["--json"])
    print(f"Command completed with exit code: {result.exit_code}")
    print(f"Output: {result.output}")
    
    if result.exception:
        print(f"Exception: {result.exception}")
        import traceback
        traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
    
    print("CLI test finished successfully!")

except Exception as e:
    print(f"Error during CLI test: {e}")
    import traceback
    traceback.print_exc()
    
print("Debug test completed.")