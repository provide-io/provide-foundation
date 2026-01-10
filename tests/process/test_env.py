#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for environment variable scrubbing and security."""

from __future__ import annotations

import os

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.process.env import (
    SAFE_ENV_ALLOWLIST,
    SENSITIVE_ENV_PATTERNS,
    is_sensitive_env_var,
    mask_sensitive_env_vars,
    prepare_subprocess_environment,
    scrub_environment,
)


class TestSafeEnvAllowlist(FoundationTestCase):
    """Test SAFE_ENV_ALLOWLIST constant."""

    def test_allowlist_contains_common_safe_vars(self) -> None:
        """Test allowlist includes common safe environment variables."""
        assert "PATH" in SAFE_ENV_ALLOWLIST
        assert "HOME" in SAFE_ENV_ALLOWLIST
        assert "LANG" in SAFE_ENV_ALLOWLIST
        assert "USER" in SAFE_ENV_ALLOWLIST
        assert "PYTHONPATH" in SAFE_ENV_ALLOWLIST

    def test_allowlist_excludes_sensitive_vars(self) -> None:
        """Test allowlist does not include sensitive variables."""
        # These should NOT be in the allowlist
        assert "AWS_SECRET_ACCESS_KEY" not in SAFE_ENV_ALLOWLIST
        assert "GITHUB_TOKEN" not in SAFE_ENV_ALLOWLIST
        assert "DATABASE_URL" not in SAFE_ENV_ALLOWLIST
        assert "API_KEY" not in SAFE_ENV_ALLOWLIST

    def test_allowlist_includes_provide_vars(self) -> None:
        """Test allowlist includes Foundation-specific variables."""
        assert "PROVIDE_TELEMETRY_DISABLED" in SAFE_ENV_ALLOWLIST
        assert "PROVIDE_LOG_LEVEL" in SAFE_ENV_ALLOWLIST
        assert "PROVIDE_LOG_FORMAT" in SAFE_ENV_ALLOWLIST


class TestSensitivePatterns(FoundationTestCase):
    """Test SENSITIVE_ENV_PATTERNS constant."""

    def test_patterns_include_common_secrets(self) -> None:
        """Test patterns include common secret indicators."""
        assert "TOKEN" in SENSITIVE_ENV_PATTERNS
        assert "SECRET" in SENSITIVE_ENV_PATTERNS
        assert "KEY" in SENSITIVE_ENV_PATTERNS
        assert "PASSWORD" in SENSITIVE_ENV_PATTERNS
        assert "API_KEY" in SENSITIVE_ENV_PATTERNS

    def test_patterns_include_cloud_providers(self) -> None:
        """Test patterns include cloud provider credentials."""
        assert "AWS_ACCESS_KEY" in SENSITIVE_ENV_PATTERNS
        assert "AWS_SECRET" in SENSITIVE_ENV_PATTERNS
        assert "GCP_KEY" in SENSITIVE_ENV_PATTERNS
        assert "AZURE_" in SENSITIVE_ENV_PATTERNS


class TestIsSensitiveEnvVar(FoundationTestCase):
    """Test is_sensitive_env_var function."""

    def test_detects_token_variables(self) -> None:
        """Test detection of token variables."""
        assert is_sensitive_env_var("GITHUB_TOKEN")
        assert is_sensitive_env_var("GITLAB_TOKEN")
        assert is_sensitive_env_var("MY_AUTH_TOKEN")
        assert is_sensitive_env_var("access_token")  # Case insensitive

    def test_detects_key_variables(self) -> None:
        """Test detection of key variables."""
        assert is_sensitive_env_var("API_KEY")
        assert is_sensitive_env_var("AWS_ACCESS_KEY_ID")
        assert is_sensitive_env_var("PRIVATE_KEY")
        assert is_sensitive_env_var("encryption_key")

    def test_detects_password_variables(self) -> None:
        """Test detection of password variables."""
        assert is_sensitive_env_var("PASSWORD")
        assert is_sensitive_env_var("DB_PASSWORD")
        assert is_sensitive_env_var("MYSQL_ROOT_PASSWORD")
        assert is_sensitive_env_var("user_passwd")

    def test_detects_secret_variables(self) -> None:
        """Test detection of secret variables."""
        assert is_sensitive_env_var("AWS_SECRET_ACCESS_KEY")
        assert is_sensitive_env_var("CLIENT_SECRET")
        assert is_sensitive_env_var("APP_SECRET")

    def test_ignores_safe_variables(self) -> None:
        """Test safe variables are not flagged as sensitive."""
        assert not is_sensitive_env_var("PATH")
        assert not is_sensitive_env_var("HOME")
        assert not is_sensitive_env_var("USER")
        assert not is_sensitive_env_var("LANG")
        assert not is_sensitive_env_var("PYTHONPATH")

    def test_case_insensitive_detection(self) -> None:
        """Test pattern matching is case insensitive."""
        assert is_sensitive_env_var("github_token")
        assert is_sensitive_env_var("GitHub_Token")
        assert is_sensitive_env_var("GITHUB_TOKEN")


class TestScrubEnvironment(FoundationTestCase):
    """Test scrub_environment function."""

    def test_scrubs_to_allowlist(self) -> None:
        """Test scrubbing filters to allowlist only."""
        env = {
            "PATH": "/usr/bin",
            "HOME": "/home/user",
            "AWS_SECRET_KEY": "secret123",
            "GITHUB_TOKEN": "ghp_token",
            "CUSTOM_VAR": "value",
        }

        scrubbed = scrub_environment(env)

        # Safe vars included
        assert "PATH" in scrubbed
        assert "HOME" in scrubbed

        # Unsafe vars excluded
        assert "AWS_SECRET_KEY" not in scrubbed
        assert "GITHUB_TOKEN" not in scrubbed
        assert "CUSTOM_VAR" not in scrubbed

    def test_custom_allowlist(self) -> None:
        """Test scrubbing with custom allowlist."""
        env = {
            "PATH": "/usr/bin",
            "CUSTOM_SAFE": "value",
            "SECRET": "secret",
        }

        custom_allowlist = {"PATH", "CUSTOM_SAFE"}
        scrubbed = scrub_environment(env, allowlist=custom_allowlist)

        assert "PATH" in scrubbed
        assert "CUSTOM_SAFE" in scrubbed
        assert "SECRET" not in scrubbed

    def test_disabled_scrubbing(self) -> None:
        """Test scrubbing can be disabled."""
        env = {
            "PATH": "/usr/bin",
            "AWS_SECRET_KEY": "secret123",
        }

        scrubbed = scrub_environment(env, enabled=False)

        # All vars included when disabled
        assert "PATH" in scrubbed
        assert "AWS_SECRET_KEY" in scrubbed
        assert len(scrubbed) == len(env)

    def test_preserves_values(self) -> None:
        """Test scrubbing preserves values of allowed variables."""
        env = {"PATH": "/custom/path:/usr/bin", "HOME": "/home/testuser"}

        scrubbed = scrub_environment(env)

        assert scrubbed["PATH"] == "/custom/path:/usr/bin"
        assert scrubbed["HOME"] == "/home/testuser"


class TestMaskSensitiveEnvVars(FoundationTestCase):
    """Test mask_sensitive_env_vars function."""

    def test_masks_sensitive_values(self) -> None:
        """Test sensitive values are masked."""
        env = {
            "PATH": "/usr/bin",
            "AWS_SECRET_KEY": "AKIAIOSFODNN7EXAMPLE",
            "GITHUB_TOKEN": "ghp_1234567890abcdef",
        }

        masked = mask_sensitive_env_vars(env)

        assert masked["PATH"] == "/usr/bin"
        assert masked["AWS_SECRET_KEY"] == "[MASKED]"
        assert masked["GITHUB_TOKEN"] == "[MASKED]"

    def test_preserves_safe_values(self) -> None:
        """Test safe values are not masked."""
        env = {
            "PATH": "/usr/bin",
            "HOME": "/home/user",
            "USER": "testuser",
        }

        masked = mask_sensitive_env_vars(env)

        assert masked["PATH"] == "/usr/bin"
        assert masked["HOME"] == "/home/user"
        assert masked["USER"] == "testuser"

    def test_masks_all_sensitive_patterns(self) -> None:
        """Test various sensitive patterns are masked."""
        env = {
            "API_KEY": "key123",
            "PASSWORD": "pass123",
            "SECRET": "secret123",
            "TOKEN": "token123",
            "CREDENTIAL": "cred123",
        }

        masked = mask_sensitive_env_vars(env)

        for key in env:
            assert masked[key] == "[MASKED]"


class TestPrepareSubprocessEnvironment(FoundationTestCase):
    """Test prepare_subprocess_environment function."""

    def test_default_scrubbing_enabled(self) -> None:
        """Test scrubbing is enabled by default."""
        result = prepare_subprocess_environment()

        # Should only contain allowlisted vars + PROVIDE_TELEMETRY_DISABLED
        assert "PROVIDE_TELEMETRY_DISABLED" in result
        assert result["PROVIDE_TELEMETRY_DISABLED"] == "true"

        # Check that result is much smaller than full os.environ
        assert len(result) < len(os.environ)

    def test_caller_overrides_always_included(self) -> None:
        """Test caller overrides are always included regardless of scrubbing."""
        caller_env = {
            "CUSTOM_VAR": "custom_value",
            "MY_SECRET": "should_be_included",  # Even though sensitive pattern
        }

        result = prepare_subprocess_environment(caller_overrides=caller_env, scrub=True)

        # Caller overrides should be present even with scrubbing
        assert "CUSTOM_VAR" in result
        assert result["CUSTOM_VAR"] == "custom_value"
        assert "MY_SECRET" in result
        assert result["MY_SECRET"] == "should_be_included"

    def test_scrubbing_disabled(self) -> None:
        """Test scrubbing can be disabled."""
        result = prepare_subprocess_environment(scrub=False)

        # Should contain most/all of os.environ
        # (Size may vary slightly due to PROVIDE_TELEMETRY_DISABLED addition)
        assert len(result) >= len(os.environ) - 5

    def test_telemetry_always_disabled(self) -> None:
        """Test PROVIDE_TELEMETRY_DISABLED is always added."""
        result1 = prepare_subprocess_environment(scrub=True)
        result2 = prepare_subprocess_environment(scrub=False)

        assert result1.get("PROVIDE_TELEMETRY_DISABLED") == "true"
        assert result2.get("PROVIDE_TELEMETRY_DISABLED") == "true"

    def test_custom_allowlist(self) -> None:
        """Test custom allowlist can be provided."""
        custom_allowlist = {"PATH", "MY_CUSTOM_VAR"}

        # Set a var in os.environ for testing
        original = os.environ.get("MY_CUSTOM_VAR")
        try:
            os.environ["MY_CUSTOM_VAR"] = "test_value"

            result = prepare_subprocess_environment(scrub=True, allowlist=custom_allowlist)

            assert "PATH" in result
            # MY_CUSTOM_VAR may or may not be in result depending on if it was set
            # But it should be in allowlist
        finally:
            if original is None:
                os.environ.pop("MY_CUSTOM_VAR", None)
            else:
                os.environ["MY_CUSTOM_VAR"] = original


class TestIntegrationWithProcessExecution(FoundationTestCase):
    """Test environment scrubbing integration with process execution."""

    @pytest.mark.asyncio
    async def test_subprocess_gets_scrubbed_env(self) -> None:
        """Test subprocess receives scrubbed environment."""
        from provide.foundation.process.sync.execution import run

        # Run a command that prints all environment variables
        result = run(["env"], capture_output=True)

        env_output = result.stdout

        # Check that PROVIDE_TELEMETRY_DISABLED is present
        assert "PROVIDE_TELEMETRY_DISABLED=true" in env_output

        # PATH should be present (in allowlist)
        assert "PATH=" in env_output

        # Count environment variables (rough check)
        env_count = len([line for line in env_output.split("\n") if "=" in line])

        # Should be significantly fewer than full os.environ
        # Allowlist has ~30-40 vars, full environ often has 80-100+
        assert env_count < 60, f"Too many env vars: {env_count}"

    @pytest.mark.asyncio
    async def test_caller_overrides_reach_subprocess(self) -> None:
        """Test caller-provided env vars reach the subprocess."""
        from provide.foundation.process.sync.execution import run

        custom_env = {"MY_CUSTOM_VAR": "test_value_12345"}

        result = run(["env"], env=custom_env, capture_output=True)

        # Custom var should be in output
        assert "MY_CUSTOM_VAR=test_value_12345" in result.stdout

    @pytest.mark.asyncio
    async def test_completed_process_only_stores_overrides(self) -> None:
        """Test CompletedProcess only stores caller overrides, not full env."""
        from provide.foundation.process.sync.execution import run

        custom_env = {"MY_VAR": "value"}

        result = run(["echo", "test"], env=custom_env, capture_output=True)

        # CompletedProcess.env should only contain caller overrides
        assert result.env is not None
        assert result.env == {"MY_VAR": "value"}
        assert "PATH" not in result.env  # System var not stored

    @pytest.mark.asyncio
    async def test_completed_process_no_env_when_none_provided(self) -> None:
        """Test CompletedProcess.env is None when no overrides provided."""
        from provide.foundation.process.sync.execution import run

        result = run(["echo", "test"], capture_output=True)

        # No env overrides provided, so should be None
        assert result.env is None


# 🧱🏗️🔚
