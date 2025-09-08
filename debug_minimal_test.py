#!/usr/bin/env python3

import os
import sys
import json
import threading
import signal

# Add the src directory to the path
sys.path.insert(0, '/Users/tim/code/gh/provide-io/provide-foundation/src')

# Set up testing environment
os.environ["CLICK_TESTING"] = "1"

def timeout_handler(signum, frame):
    print("TIMEOUT: Test is hanging!")
    import traceback
    traceback.print_stack(frame)
    sys.exit(1)

# Set up signal handler for timeout debugging
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(15)  # 15 second timeout

print("Starting minimal debug test...")

try:
    print("1. Importing modules...")
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
    
    print("2. All imports successful")
    
    print("3. Creating simple test CLI...")
    @click.command()
    @flexible_options
    @output_options
    @pass_context  
    def simple_cmd(ctx: Context, **kwargs) -> None:
        """Simple test command."""
        print("INSIDE SIMPLE COMMAND")
        for key, value in kwargs.items():
            if value is not None:
                setattr(ctx, key, value)
        setup_cli_logging(ctx)
        print("CLI LOGGING SETUP COMPLETE")
        click.echo("Simple test successful")
    
    print("4. Test command created")
    
    print("5. Creating CLI runner...")
    runner = CliTestRunner()
    print("6. CLI runner created")
    
    print("7. About to invoke command...")
    result = runner.invoke(simple_cmd, ["--json"])
    print("8. Command invoked")
    print(f"Exit code: {result.exit_code}")
    print(f"Output: {result.output}")
    
    if result.exception:
        print(f"Exception: {result.exception}")
        import traceback
        traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
    
    print("9. Test completed successfully!")

except KeyboardInterrupt:
    print("Test interrupted by user")
    sys.exit(1)
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    signal.alarm(0)  # Cancel timeout
    
print("Debug test completed.")