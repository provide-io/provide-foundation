# provide/foundation/cli/commands/logs/send.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import sys
from typing import Any

from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import (
    build_attributes_from_args,
    get_message_from_stdin,
    requires_click,
)
from provide.foundation.cli.shutdown import with_cleanup
from provide.foundation.console.output import perr, pout
from provide.foundation.logger import get_logger
from provide.foundation.process import exit_error, exit_success

"""Send logs command for Foundation CLI."""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__get_message_from_input__mutmut_orig(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_1(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 1

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_2(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = None

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_3(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 or sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_4(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code == 0 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_5(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 1 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_6(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo(None, err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_7(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=None)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_8(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo(err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_9(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", )

    return stdin_message, error_code


def x__get_message_from_input__mutmut_10(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("XXError: No message provided. Use -m or pipe input.XX", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_11(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("error: no message provided. use -m or pipe input.", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_12(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("ERROR: NO MESSAGE PROVIDED. USE -M OR PIPE INPUT.", err=True)

    return stdin_message, error_code


def x__get_message_from_input__mutmut_13(message: str | None) -> tuple[str | None, int]:
    """Get message from argument or stdin. Returns (message, error_code)."""
    if message:
        return message, 0

    # Try to read from stdin using shared helper
    stdin_message, error_code = get_message_from_stdin()

    # If stdin is TTY (no piped input), show helpful error
    if error_code != 0 and sys.stdin.isatty():
        click.echo("Error: No message provided. Use -m or pipe input.", err=False)

    return stdin_message, error_code

x__get_message_from_input__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_message_from_input__mutmut_1': x__get_message_from_input__mutmut_1, 
    'x__get_message_from_input__mutmut_2': x__get_message_from_input__mutmut_2, 
    'x__get_message_from_input__mutmut_3': x__get_message_from_input__mutmut_3, 
    'x__get_message_from_input__mutmut_4': x__get_message_from_input__mutmut_4, 
    'x__get_message_from_input__mutmut_5': x__get_message_from_input__mutmut_5, 
    'x__get_message_from_input__mutmut_6': x__get_message_from_input__mutmut_6, 
    'x__get_message_from_input__mutmut_7': x__get_message_from_input__mutmut_7, 
    'x__get_message_from_input__mutmut_8': x__get_message_from_input__mutmut_8, 
    'x__get_message_from_input__mutmut_9': x__get_message_from_input__mutmut_9, 
    'x__get_message_from_input__mutmut_10': x__get_message_from_input__mutmut_10, 
    'x__get_message_from_input__mutmut_11': x__get_message_from_input__mutmut_11, 
    'x__get_message_from_input__mutmut_12': x__get_message_from_input__mutmut_12, 
    'x__get_message_from_input__mutmut_13': x__get_message_from_input__mutmut_13
}

def _get_message_from_input(*args, **kwargs):
    result = _mutmut_trampoline(x__get_message_from_input__mutmut_orig, x__get_message_from_input__mutmut_mutants, args, kwargs)
    return result 

_get_message_from_input.__signature__ = _mutmut_signature(x__get_message_from_input__mutmut_orig)
x__get_message_from_input__mutmut_orig.__name__ = 'x__get_message_from_input'


def x__send_log_entry__mutmut_orig(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_1(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = None

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_2(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(None)

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_3(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name and "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_4(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "XXcli.sendXX")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_5(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "CLI.SEND")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_6(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = None
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_7(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["XXtrace_idXX"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_8(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["TRACE_ID"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_9(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = None

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_10(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["XXspan_idXX"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_11(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["SPAN_ID"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_12(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = None

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_13(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(None, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_14(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, None, logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_15(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), None)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_16(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_17(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_18(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), )

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_19(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.upper(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_20(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(None, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_21(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(**attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_22(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, )

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_23(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout(None, color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_24(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color=None)
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_25(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout(color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_26(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", )
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_27(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("XX✓ Log sent successfullyXX", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_28(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_29(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ LOG SENT SUCCESSFULLY", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_30(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="XXgreenXX")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_31(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="GREEN")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_32(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 1
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 1


def x__send_log_entry__mutmut_33(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(None, color="red")
        return 1


def x__send_log_entry__mutmut_34(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color=None)
        return 1


def x__send_log_entry__mutmut_35(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(color="red")
        return 1


def x__send_log_entry__mutmut_36(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", )
        return 1


def x__send_log_entry__mutmut_37(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="XXredXX")
        return 1


def x__send_log_entry__mutmut_38(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="RED")
        return 1


def x__send_log_entry__mutmut_39(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any],
    trace_id: str | None,
    span_id: str | None,
) -> int:
    """Send the log entry using the main FoundationLogger."""
    try:
        # Get a logger instance, optionally scoped to the service name
        logger = get_logger(service_name or "cli.send")

        # Add trace context to attributes if provided
        if trace_id:
            attributes["trace_id"] = trace_id
        if span_id:
            attributes["span_id"] = span_id

        # Get the appropriate log method (info, error, etc.)
        log_method = getattr(logger, level.lower(), logger.info)

        # Emit the log
        log_method(message, **attributes)

        pout("✓ Log sent successfully", color="green")
        return 0
    except Exception as e:
        perr(f"✗ Failed to send log: {e}", color="red")
        return 2

x__send_log_entry__mutmut_mutants : ClassVar[MutantDict] = {
'x__send_log_entry__mutmut_1': x__send_log_entry__mutmut_1, 
    'x__send_log_entry__mutmut_2': x__send_log_entry__mutmut_2, 
    'x__send_log_entry__mutmut_3': x__send_log_entry__mutmut_3, 
    'x__send_log_entry__mutmut_4': x__send_log_entry__mutmut_4, 
    'x__send_log_entry__mutmut_5': x__send_log_entry__mutmut_5, 
    'x__send_log_entry__mutmut_6': x__send_log_entry__mutmut_6, 
    'x__send_log_entry__mutmut_7': x__send_log_entry__mutmut_7, 
    'x__send_log_entry__mutmut_8': x__send_log_entry__mutmut_8, 
    'x__send_log_entry__mutmut_9': x__send_log_entry__mutmut_9, 
    'x__send_log_entry__mutmut_10': x__send_log_entry__mutmut_10, 
    'x__send_log_entry__mutmut_11': x__send_log_entry__mutmut_11, 
    'x__send_log_entry__mutmut_12': x__send_log_entry__mutmut_12, 
    'x__send_log_entry__mutmut_13': x__send_log_entry__mutmut_13, 
    'x__send_log_entry__mutmut_14': x__send_log_entry__mutmut_14, 
    'x__send_log_entry__mutmut_15': x__send_log_entry__mutmut_15, 
    'x__send_log_entry__mutmut_16': x__send_log_entry__mutmut_16, 
    'x__send_log_entry__mutmut_17': x__send_log_entry__mutmut_17, 
    'x__send_log_entry__mutmut_18': x__send_log_entry__mutmut_18, 
    'x__send_log_entry__mutmut_19': x__send_log_entry__mutmut_19, 
    'x__send_log_entry__mutmut_20': x__send_log_entry__mutmut_20, 
    'x__send_log_entry__mutmut_21': x__send_log_entry__mutmut_21, 
    'x__send_log_entry__mutmut_22': x__send_log_entry__mutmut_22, 
    'x__send_log_entry__mutmut_23': x__send_log_entry__mutmut_23, 
    'x__send_log_entry__mutmut_24': x__send_log_entry__mutmut_24, 
    'x__send_log_entry__mutmut_25': x__send_log_entry__mutmut_25, 
    'x__send_log_entry__mutmut_26': x__send_log_entry__mutmut_26, 
    'x__send_log_entry__mutmut_27': x__send_log_entry__mutmut_27, 
    'x__send_log_entry__mutmut_28': x__send_log_entry__mutmut_28, 
    'x__send_log_entry__mutmut_29': x__send_log_entry__mutmut_29, 
    'x__send_log_entry__mutmut_30': x__send_log_entry__mutmut_30, 
    'x__send_log_entry__mutmut_31': x__send_log_entry__mutmut_31, 
    'x__send_log_entry__mutmut_32': x__send_log_entry__mutmut_32, 
    'x__send_log_entry__mutmut_33': x__send_log_entry__mutmut_33, 
    'x__send_log_entry__mutmut_34': x__send_log_entry__mutmut_34, 
    'x__send_log_entry__mutmut_35': x__send_log_entry__mutmut_35, 
    'x__send_log_entry__mutmut_36': x__send_log_entry__mutmut_36, 
    'x__send_log_entry__mutmut_37': x__send_log_entry__mutmut_37, 
    'x__send_log_entry__mutmut_38': x__send_log_entry__mutmut_38, 
    'x__send_log_entry__mutmut_39': x__send_log_entry__mutmut_39
}

def _send_log_entry(*args, **kwargs):
    result = _mutmut_trampoline(x__send_log_entry__mutmut_orig, x__send_log_entry__mutmut_mutants, args, kwargs)
    return result 

_send_log_entry.__signature__ = _mutmut_signature(x__send_log_entry__mutmut_orig)
x__send_log_entry__mutmut_orig.__name__ = 'x__send_log_entry'


@click.command("send")
@click.option(
    "--message",
    "-m",
    help="Log message to send (reads from stdin if not provided)",
)
@click.option(
    "--level",
    "-l",
    type=click.Choice(["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level",
)
@click.option(
    "--service",
    "-s",
    "service_name",
    help="Service name (uses config default if not provided)",
)
@click.option(
    "--json",
    "-j",
    "json_attrs",
    help="Additional attributes as JSON",
)
@click.option(
    "--attr",
    "-a",
    multiple=True,
    help="Additional attributes as key=value pairs",
)
@click.option(
    "--trace-id",
    help="Explicit trace ID to use",
)
@click.option(
    "--span-id",
    help="Explicit span ID to use",
)
@click.pass_context
@requires_click
@with_cleanup
def send_command(
    ctx: click.Context,
    message: str | None,
    level: str,
    service_name: str | None,
    json_attrs: str | None,
    attr: tuple[str, ...],
    trace_id: str | None,
    span_id: str | None,
) -> int | None:
    """Send a log entry to OpenObserve.

    Examples:
        # Send a simple log
        foundation logs send -m "User logged in" -l INFO

        # Send with attributes
        foundation logs send -m "Payment processed" --attr user_id=123 --attr amount=99.99

        # Send from stdin
        echo "Application started" | foundation logs send -l INFO

        # Send with JSON attributes
        foundation logs send -m "Error occurred" -j '{"error_code": 500, "path": "/api/users"}'

    """
    # Get message from input
    final_message, error_code = _get_message_from_input(message)
    if error_code != 0:
        exit_error("No message provided", code=error_code)

    # Build attributes using shared helper
    attributes, error_code = build_attributes_from_args(json_attrs, attr)
    if error_code != 0:
        exit_error("Invalid attributes", code=error_code)

    # Send the log entry
    result = _send_log_entry(
        final_message,  # type: ignore[arg-type]
        level,
        service_name,
        attributes,
        trace_id,
        span_id,
    )

    if result == 0:
        exit_success()
    else:
        exit_error("Failed to send log", code=result)

    return None


# <3 🧱🤝💻🪄
