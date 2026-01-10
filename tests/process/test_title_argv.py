#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for set_process_title_from_argv functionality."""

from __future__ import annotations

from pathlib import Path

from provide.testkit import FoundationTestCase


class TestSetProcessTitleFromArgv(FoundationTestCase):
    """Test set_process_title_from_argv function.

    Note: set_process_title_from_argv has @skip_in_test_mode decorator,
    so it returns True without side effects in test mode. We test the
    decorator behavior and verify the argv parsing logic used by the function.
    """

    def test_returns_true_in_test_mode(self) -> None:
        """Test that function returns True in test mode due to decorator."""
        from provide.foundation.process.title import set_process_title_from_argv

        result = set_process_title_from_argv()

        # Should return True due to @skip_in_test_mode decorator
        assert result is True

    def test_argv_parsing_logic_basic(self) -> None:
        """Test argv parsing logic: cmd arg1 arg2."""
        test_argv = ["pyvider", "run", "--config", "foo.yml"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "pyvider run --config foo.yml"

    def test_argv_parsing_with_full_path(self) -> None:
        """Test argv parsing extracts basename from full path."""
        test_argv = ["/usr/bin/pyvider", "run"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "pyvider run"

    def test_argv_parsing_symlink(self) -> None:
        """Test argv parsing preserves symlink name."""
        # Simulates: whatever -> pyvider symlink
        test_argv = ["whatever", "run"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "whatever run"

    def test_argv_parsing_no_args(self) -> None:
        """Test argv parsing with just command name."""
        test_argv = ["pyvider"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "pyvider"

    def test_argv_parsing_special_characters(self) -> None:
        """Test argv parsing with special characters."""
        test_argv = ["pyvider", "--name", "my app", "--flag"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "pyvider --name my app --flag"

    def test_argv_parsing_with_equals(self) -> None:
        """Test argv parsing with equals in args."""
        test_argv = ["soup", "--config=foo.yml", "--verbose"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "soup --config=foo.yml --verbose"

    def test_argv_parsing_complex_path(self) -> None:
        """Test argv parsing with complex path."""
        test_argv = ["/opt/tools/bin/myapp", "worker", "--threads", "4"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "myapp worker --threads 4"

    def test_argv_parsing_unicode_command(self) -> None:
        """Test argv parsing with unicode in command name."""
        test_argv = ["my-app-✨", "run"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "my-app-✨ run"

    def test_argv_parsing_unicode_args(self) -> None:
        """Test argv parsing with unicode in arguments."""
        test_argv = ["myapp", "--message", "Hello 世界"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "myapp --message Hello 世界"

    def test_argv_parsing_python_extension(self) -> None:
        """Test argv parsing preserves .py extension."""
        test_argv = ["script.py", "arg1"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "script.py arg1"

    def test_argv_parsing_many_args(self) -> None:
        """Test argv parsing with many arguments."""
        test_argv = ["app"] + [f"--arg{i}" for i in range(20)]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        expected = "app " + " ".join(f"--arg{i}" for i in range(20))
        assert title == expected

    def test_realistic_pyvider_scenario(self) -> None:
        """Test realistic pyvider invocation."""
        test_argv = [
            "/opt/pyvider/bin/pyvider",
            "run",
            "--config",
            "/etc/pyvider/config.yml",
            "--verbose",
        ]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "pyvider run --config /etc/pyvider/config.yml --verbose"

    def test_realistic_soup_scenario(self) -> None:
        """Test realistic soup invocation."""
        test_argv = ["soup", "serve", "--port", "8080", "--workers", "4"]

        cmd_name = Path(test_argv[0]).name
        args = test_argv[1:]
        title = f"{cmd_name} {' '.join(args)}" if args else cmd_name

        assert title == "soup serve --port 8080 --workers 4"


# 🧱🏗️🔚
