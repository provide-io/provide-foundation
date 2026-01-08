#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""CLI Dogfooding Example - Using Foundation's Own Features

This example demonstrates how to build CLI applications that "dogfood"
Foundation's own features instead of using external libraries or ad-hoc
implementations.

Dogfooding Benefits:
1. Consistent behavior across applications
2. Built-in error handling and logging
3. Better testing and validation
4. Reduced external dependencies
5. Demonstrates best practices

Features Demonstrated:

1. Environment Variables (utils/environment):
   - get_str(), get_int(), get_bool() for typed access
   - Better than os.environ.get() with manual parsing

2. Structured Configuration (config):
   - RuntimeConfig and env_field for type-safe configuration
   - Better than manual environment variable parsing

3. File I/O (file/atomic and file/safe):
   - atomic_write_text() to prevent file corruption
   - safe_read_text() for error handling
   - Better than direct Path.open()

4. Process Execution (process/sync/execution):
   - run() and run_simple() with consistent error handling
   - Better than subprocess.run() directly

5. Parsing (parsers/primitives):
   - parse_typed_value() for CLI argument parsing
   - Better than manual type detection

6. Error Handling (errors/decorators):
   - @resilient decorator for graceful degradation
   - Better than manual try/except

7. Console Output (console/output):
   - pout() and perr() for JSON mode support
   - Better than print() for CLI output

8. Cryptography (crypto/hashing):
   - hash_file() for checksums
   - Better than manual hashlib usage

Usage:
    python examples/cli/02_dogfooding_cli.py config-demo
    python examples/cli/02_dogfooding_cli.py file-demo
    python examples/cli/02_dogfooding_cli.py process-demo
    python examples/cli/02_dogfooding_cli.py parse-demo --value "123"
    python examples/cli/02_dogfooding_cli.py hash-demo --file README.md

"""

from __future__ import annotations

from pathlib import Path

from attrs import define

from provide.foundation.cli import echo_error, echo_info, echo_success, echo_warning
from provide.foundation.config import RuntimeConfig, env_field
from provide.foundation.console.output import perr, pout
from provide.foundation.crypto.hashing import hash_file
from provide.foundation.errors.decorators import resilient
from provide.foundation.file.atomic import atomic_write_text
from provide.foundation.file.safe import safe_read_text
from provide.foundation.hub import Hub, register_command
from provide.foundation.logger import get_logger
from provide.foundation.parsers.primitives import parse_bool
from provide.foundation.parsers.typed import parse_typed_value
from provide.foundation.process.sync.execution import run, run_simple
from provide.foundation.utils.environment import get_bool, get_int, get_str

log = get_logger(__name__)

# ==============================================================================
# STRUCTURED CONFIGURATION (Dogfooding: config.BaseConfig)
# ==============================================================================


@define
class AppConfig(RuntimeConfig):
    """Application configuration using Foundation's config system.

    Better than manual os.environ.get() because:
    - Type-safe with attrs validation
    - Supports file:// prefix for secrets
    - Automatic parsing based on field types
    - IDE autocomplete
    - Loads from environment variables via from_env()
    """

    app_name: str = env_field(env_var="APP_NAME", default="dogfooding-demo")
    port: int = env_field(env_var="APP_PORT", default=8000, parser=int)
    debug: bool = env_field(env_var="APP_DEBUG", default=False, parser=parse_bool)
    workers: int = env_field(env_var="APP_WORKERS", default=4, parser=int)
    log_level: str = env_field(env_var="LOG_LEVEL", default="INFO")


# ==============================================================================
# COMMANDS DEMONSTRATING DOGFOODING
# ==============================================================================


@register_command("config-demo", category="demo")
def config_demo_command() -> None:
    """Demonstrate structured configuration vs. ad-hoc parsing.

    Shows:
    - Foundation's BaseConfig with env_field
    - Direct environment variable access with utils/environment
    - Better than os.environ.get() with manual parsing
    """
    pout("=" * 60)

    # Method 1: Structured configuration class (best for application config)
    pout("\n1️⃣  Structured Configuration (RuntimeConfig):")
    pout("-" * 60)
    config = AppConfig.from_env()
    pout(f"   App Name:   {config.app_name}")
    pout(f"   Port:       {config.port}")
    pout(f"   Debug:      {config.debug}")
    pout(f"   Workers:    {config.workers}")
    pout(f"   Log Level:  {config.log_level}")

    # Method 2: Direct typed access (good for simple scripts)
    pout("\n2️⃣  Direct Typed Access (utils/environment):")
    pout("-" * 60)
    max_retries = get_int("MAX_RETRIES", default=3)
    timeout = get_int("TIMEOUT", default=30)
    verbose = get_bool("VERBOSE", default=False)
    api_url = get_str("API_URL", default="https://api.example.com")

    pout(f"   Max Retries: {max_retries}")
    pout(f"   Timeout:     {timeout}s")
    pout(f"   Verbose:     {verbose}")
    pout(f"   API URL:     {api_url}")


@register_command("file-demo", category="demo")
def file_demo_command() -> None:
    """Demonstrate safe file I/O operations.

    Shows:
    - atomic_write_text() to prevent corruption
    - safe_read_text() with error handling
    - hash_file() for checksums
    """
    pout("=" * 60)

    demo_file = Path("/tmp/dogfooding_demo.txt")

    # Write atomically (prevents corruption on failure)
    pout("\n1️⃣  Atomic Write:")
    pout("-" * 60)
    content = "Hello from Foundation!\nAtomic writes prevent corruption."

    try:
        atomic_write_text(demo_file, content)
    except Exception as e:
        perr(f"   ❌ Write failed: {e}")
        return

    # Read safely with error handling
    pout("\n2️⃣  Safe Read:")
    pout("-" * 60)
    read_content = safe_read_text(demo_file)
    if read_content:
        pout(f"   ✅ Read {len(read_content)} characters")
    else:
        perr("   ❌ Read failed")
        return

    # Hash verification
    pout("\n3️⃣  File Hashing:")
    pout("-" * 60)
    hash_file(demo_file, algorithm="sha256")

    # Cleanup
    demo_file.unlink()


@register_command("process-demo", category="demo")
def process_demo_command() -> None:
    """Demonstrate process execution with Foundation.

    Shows:
    - run() for full control
    - run_simple() for simple output
    - Better than subprocess.run() directly
    """
    pout("=" * 60)

    # Simple command (returns stdout)
    pout("\n1️⃣  Simple Command (run_simple):")
    pout("-" * 60)
    try:
        run_simple(["echo", "Hello from Foundation!"])
    except Exception as e:
        perr(f"   ❌ Command failed: {e}")

    # Full control with run()
    pout("\n2️⃣  Full Control (run):")
    pout("-" * 60)
    try:
        run(
            ["python", "-c", "print('Python subprocess')"],
            capture_output=True,
            check=True,
        )
    except Exception as e:
        perr(f"   ❌ Command failed: {e}")


@register_command("parse-demo", category="demo")
def parse_demo_command(value: str = "42") -> None:
    """Demonstrate typed value parsing.

    Shows:
    - parse_typed_value() with type hints
    - Better than manual value.isdigit() checks

    Args:
        value: Value to parse (try: "123", "true", "3.14", "hello")
    """
    pout("\n🔤 Parsing Dogfooding Demo\n")
    pout("=" * 60)

    # Examples of parsing to specific types
    test_cases = [
        ("123", int, "Integer"),
        ("true", bool, "Boolean"),
        ("3.14", float, "Float"),
        ("hello", str, "String"),
        ("1,2,3", list, "List"),
        ('{"key": "value"}', dict, "Dict"),
        (value, str, f"User value '{value}'"),
    ]

    pout("\nParsing values with type hints:")
    pout("-" * 60)

    for test_val, target_type, description in test_cases:
        try:
            parsed = parse_typed_value(test_val, target_type)
            pout(f"   {description:20s} '{test_val}' → {type(parsed).__name__}: {parsed}")
        except Exception as e:
            perr(f"   {description:20s} '{test_val}' → Error: {e}")


@register_command("hash-demo", category="demo")
def hash_demo_command(file: str = "README.md") -> None:
    """Demonstrate file hashing.

    Shows:
    - hash_file() for checksums
    - Better than manual hashlib usage
    - Supports multiple algorithms

    Args:
        file: File to hash
    """
    pout("\n🔐 Hashing Dogfooding Demo\n")
    pout("=" * 60)

    file_path = Path(file)

    if not file_path.exists():
        perr(f"\n❌ File not found: {file}")
        perr("   Try: --file README.md\n")
        return

    pout(f"\nHashing file: {file_path}")
    pout("-" * 60)

    # Different algorithms
    algorithms = ["md5", "sha256", "sha512"]

    for algo in algorithms:
        try:
            file_hash = hash_file(file_path, algorithm=algo)
            pout(f"   {algo.upper():8s}: {file_hash}")
        except Exception as e:
            perr(f"   {algo.upper():8s}: Error: {e}")


@register_command("error-demo", category="demo")
def error_demo_command() -> None:
    """Demonstrate error handling with @resilient.

    Shows:
    - @resilient decorator for graceful degradation
    - Better than manual try/except blocks
    """
    pout("\n🛡️  Error Handling Dogfooding Demo\n")
    pout("=" * 60)

    @resilient(
        context_provider=lambda: {"operation": "demo"},
        default_return=None,
    )
    def risky_operation(should_fail: bool = False) -> str | None:
        """Operation that might fail."""
        if should_fail:
            raise ValueError("Simulated failure")
        return "Success!"

    pout("\n1️⃣  Successful Operation:")
    pout("-" * 60)
    result = risky_operation(should_fail=False)

    pout("\n2️⃣  Failed Operation (graceful degradation):")
    pout("-" * 60)
    result = risky_operation(should_fail=True)
    pout(f"   ⚠️  Result: {result} (returned default)")


@register_command("output-demo", category="demo")
def output_demo_command() -> None:
    """Demonstrate console output helpers.

    Shows:
    - pout() and perr() for JSON mode support
    - echo_* helpers for styled output
    - Better than print() for CLI applications
    """
    pout("\n📤 Output Dogfooding Demo\n")
    pout("=" * 60)

    pout("\n1️⃣  Standard Output (pout):")
    pout("-" * 60)
    pout("   This is standard output")
    pout("   Supports JSON output mode")

    pout("\n2️⃣  Error Output (perr):")
    pout("-" * 60)
    perr("   This is error output")
    perr("   Also supports JSON mode")

    pout("\n3️⃣  Styled Output (echo_*):")
    pout("-" * 60)
    echo_info("   Info message")
    echo_success("   Success message")
    echo_warning("   Warning message")
    echo_error("   Error message")


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================


def create_dogfooding_cli() -> object:
    """Create the dogfooding demo CLI application."""
    hub = Hub()

    cli = hub.create_cli(
        name="dogfooding-demo",
        version="1.0.0",
        help="Foundation Dogfooding Demo - Using Foundation's Own Features",
    )

    return cli


if __name__ == "__main__":
    # Create and run the CLI
    cli = create_dogfooding_cli()
    cli()

# 🧱🏗️🔚
