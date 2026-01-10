#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Basic coverage tests for CLI main module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest


class TestCLIMainCoverage(FoundationTestCase):
    """Basic coverage tests for CLI main module."""

    def test_main_imports_successfully(self) -> None:
        """Test that main module can be imported."""
        from provide.foundation.cli import main

        assert main is not None

    def test_require_click_function_exists(self) -> None:
        """Test _require_click function exists."""
        from provide.foundation.cli.main import _require_click

        assert _require_click is not None
        assert callable(_require_click)

    def test_require_click_raises_when_no_click(self) -> None:
        """Test _require_click raises ImportError when click not available."""
        from provide.foundation.cli.main import _HAS_CLICK, _require_click

        if not _HAS_CLICK:
            with pytest.raises(ImportError, match="CLI requires optional dependencies"):
                _require_click()
        else:
            # If click is available, function should not raise
            _require_click()  # Should not raise

    def test_has_click_flag_is_boolean(self) -> None:
        """Test _HAS_CLICK flag is a boolean."""
        from provide.foundation.cli.main import _HAS_CLICK

        assert isinstance(_HAS_CLICK, bool)

    def test_cli_group_available_when_click_present(self) -> None:
        """Test CLI group is available when click is installed."""
        try:
            import click  # noqa: F401

            from provide.foundation.cli.main import cli

            assert cli is not None
            assert callable(cli)
        except ImportError:
            pytest.skip("Click not available")

    def test_cli_group_properties(self) -> None:
        """Test CLI group has expected properties."""
        try:
            from provide.foundation.cli.main import cli

            # Check if it's a click group
            assert hasattr(cli, "commands") or callable(cli)
        except ImportError:
            pytest.skip("Click not available")

    def test_module_has_expected_attributes(self) -> None:
        """Test module has expected attributes."""
        from provide.foundation.cli import main

        # Should have these key attributes
        assert hasattr(main, "_HAS_CLICK")
        assert hasattr(main, "_require_click")


# 🧱🏗️🔚
