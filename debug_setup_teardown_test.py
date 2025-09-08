#!/usr/bin/env python3

import os
import sys
import json

# Add the src directory to the path
sys.path.insert(0, '/Users/tim/code/gh/provide-io/provide-foundation/src')

# Set up testing environment
os.environ["CLICK_TESTING"] = "1"

print("Starting setup/teardown debug test...")

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
    
    def setup_method():
        """Set up each test method."""
        print("=== SETUP METHOD START ===")
        os.environ["CLICK_TESTING"] = "1"
        # Reset Foundation state before each test to avoid conflicts
        from provide.foundation.testing import reset_foundation_setup_for_testing

        reset_foundation_setup_for_testing()
        print("=== SETUP METHOD END ===")

    def teardown_method():
        """Clean up after each test method."""
        print("=== TEARDOWN METHOD START ===")
        os.environ.pop("CLICK_TESTING", None)
        # Clean up again after the test
        from provide.foundation.testing import reset_foundation_setup_for_testing

        reset_foundation_setup_for_testing()
        print("=== TEARDOWN METHOD END ===")

    def create_test_cli():
        """Create a test CLI with all features."""

        @click.group(invoke_without_command=True)
        @flexible_options
        @output_options
        @pass_context
        def cli(ctx: Context, **kwargs) -> None:
            """Test CLI application."""
            for key, value in kwargs.items():
                if value is not None:
                    setattr(ctx, key, value)
            # Configure logging once at the top level.
            setup_cli_logging(ctx)

            click_ctx = click.get_current_context()
            if click_ctx.invoked_subcommand is None:
                logger = get_logger(__name__)
                logger.info("CLI root command executed.")

        @cli.command()
        @pass_context
        def status(ctx: Context) -> None:
            """Show application status."""
            # No need to re-configure logging.
            logger = get_logger(__name__)
            logger.debug("Checking status")
            if ctx.json_output:
                click.echo(json.dumps({"status": "healthy", "uptime": 3600}))
            else:
                if not ctx.no_emoji:
                    click.echo("🟢 Application is healthy")
                else:
                    click.echo("Application is healthy")

        return cli
    
    def test_function():
        """Test that options work at the group level."""
        print("=== TEST FUNCTION START ===")
        cli = create_test_cli()
        runner = CliTestRunner()
        result = runner.invoke(cli, ["--log-level", "DEBUG", "--json", "status"])
        assert result.exit_code == 0
        print(f"Test result: {result.exit_code}")
        print(f"Output: {result.output}")
        output = json.loads(result.output.strip().split("\n")[-1])
        assert output["status"] == "healthy"
        print("=== TEST FUNCTION END ===")
    
    # Simulate pytest behavior
    print("Calling setup_method...")
    setup_method()
    
    print("Calling test function...")
    test_function()
    
    print("Calling teardown_method...")
    import time
    time.sleep(1)  # Give some time
    teardown_method()
    
    print("Test completed successfully!")

except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()
    
print("Debug test completed.")