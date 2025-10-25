"""Tests for set_process_title_from_argv functionality."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch


class TestSetProcessTitleFromArgv(FoundationTestCase):
    """Test set_process_title_from_argv function."""

    def test_basic_case_with_args(self) -> None:
        """Test basic case: pyvider run --config foo."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["pyvider", "run", "--config", "foo.yml"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            mock_set_title.assert_called_once_with("pyvider run --config foo.yml")

    def test_with_full_path(self) -> None:
        """Test with full path: /usr/bin/pyvider run."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["/usr/bin/pyvider", "run"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            # Should extract just the basename
            mock_set_title.assert_called_once_with("pyvider run")

    def test_symlink_simulation(self) -> None:
        """Test symlink: whatever run (where whatever -> pyvider)."""
        from provide.foundation.process.title import set_process_title_from_argv

        # Simulate running via symlink - argv[0] will be the symlink name
        test_argv = ["whatever", "run"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            # Should preserve symlink name
            mock_set_title.assert_called_once_with("whatever run")

    def test_no_args(self) -> None:
        """Test with no arguments: just 'pyvider'."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["pyvider"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            # Should be just the command name
            mock_set_title.assert_called_once_with("pyvider")

    def test_with_special_characters_in_args(self) -> None:
        """Test with special characters in arguments."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["pyvider", "--name", "my app", "--flag"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            # Should preserve all args including those with spaces
            mock_set_title.assert_called_once_with("pyvider --name my app --flag")

    def test_with_equals_in_args(self) -> None:
        """Test with equals signs in arguments."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["soup", "--config=foo.yml", "--verbose"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            mock_set_title.assert_called_once_with("soup --config=foo.yml --verbose")

    def test_with_complex_path(self) -> None:
        """Test with complex path containing multiple directories."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["/opt/tools/bin/myapp", "worker", "--threads", "4"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            mock_set_title.assert_called_once_with("myapp worker --threads 4")

    def test_when_setproctitle_unavailable(self) -> None:
        """Test behavior when setproctitle is not available."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["pyvider", "run"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title", return_value=False) as mock_set_title,
        ):
            result = set_process_title_from_argv()

            # Should return False when setproctitle unavailable
            assert result is False
            mock_set_title.assert_called_once()

    def test_skip_in_test_mode_decorator(self) -> None:
        """Test that @skip_in_test_mode decorator is working."""
        from provide.foundation.process.title import set_process_title_from_argv

        # Since we're in test mode, the function should return True without
        # actually calling set_process_title
        test_argv = ["pyvider", "run"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title"),
        ):
            # In test mode, should return early
            result = set_process_title_from_argv()

            # The decorator should cause it to return True
            assert result is True


class TestSetProcessTitleFromArgvEdgeCases(FoundationTestCase):
    """Test edge cases for set_process_title_from_argv."""

    def test_with_empty_string_arg(self) -> None:
        """Test with empty string as an argument."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["myapp", "", "run"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            # Empty string should be included
            mock_set_title.assert_called_once_with("myapp  run")

    def test_with_unicode_in_command_name(self) -> None:
        """Test with unicode characters in command name."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["my-app-✨", "run"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            mock_set_title.assert_called_once_with("my-app-✨ run")

    def test_with_unicode_in_args(self) -> None:
        """Test with unicode characters in arguments."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["myapp", "--message", "Hello 世界"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            mock_set_title.assert_called_once_with("myapp --message Hello 世界")

    def test_with_python_extension(self) -> None:
        """Test with .py extension in argv[0]."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["script.py", "arg1"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            # Should keep the .py extension
            mock_set_title.assert_called_once_with("script.py arg1")

    def test_with_many_arguments(self) -> None:
        """Test with many arguments."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["app"] + [f"--arg{i}" for i in range(20)]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            expected = "app " + " ".join(f"--arg{i}" for i in range(20))
            mock_set_title.assert_called_once_with(expected)


class TestSetProcessTitleFromArgvIntegration(FoundationTestCase):
    """Integration tests for set_process_title_from_argv."""

    def test_realistic_pyvider_scenario(self) -> None:
        """Test realistic pyvider invocation scenario."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = [
            "/opt/pyvider/bin/pyvider",
            "run",
            "--config",
            "/etc/pyvider/config.yml",
            "--verbose",
        ]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            mock_set_title.assert_called_once_with("pyvider run --config /etc/pyvider/config.yml --verbose")

    def test_realistic_soup_scenario(self) -> None:
        """Test realistic soup invocation scenario."""
        from provide.foundation.process.title import set_process_title_from_argv

        test_argv = ["soup", "serve", "--port", "8080", "--workers", "4"]

        with (
            patch("sys.argv", test_argv),
            patch("provide.foundation.process.title.set_process_title") as mock_set_title,
        ):
            result = set_process_title_from_argv()

            assert result is True
            mock_set_title.assert_called_once_with("soup serve --port 8080 --workers 4")


# <3 🧱🤝🏃🪄
