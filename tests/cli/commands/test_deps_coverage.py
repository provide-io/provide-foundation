"""Comprehensive tests for cli/commands/deps.py module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys


class TestDepsCommandWithClick:
    """Test deps command when click is available."""
    
    def test_deps_command_exists(self):
        """Test that deps_command is exported."""
        from provide.foundation.cli.commands.deps import deps_command
        assert deps_command is not None
    
    def test_deps_command_with_click(self):
        """Test deps command when click is available."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            with patch('provide.foundation.cli.commands.deps.click') as mock_click:
                mock_command = Mock()
                mock_click.command.return_value = lambda f: f
                mock_click.option.return_value = lambda f: f
                
                # Re-import to get the decorated version
                import importlib
                import provide.foundation.cli.commands.deps as deps_module
                importlib.reload(deps_module)
                
                assert deps_module.deps_command is not None
    
    def test_deps_command_check_specific_available(self):
        """Test checking specific available dependency."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            from provide.foundation.cli.commands.deps import deps_command
            
            with patch('provide.foundation.utils.deps.has_dependency', return_value=True):
                with patch('builtins.print') as mock_print:
                    with pytest.raises(SystemExit) as exc_info:
                        # Simulate click calling the function
                        deps_command.callback(quiet=False, check='crypto')
                    
                    assert exc_info.value.code == 0
                    mock_print.assert_called_once_with("✅ crypto: Available")
    
    def test_deps_command_check_specific_missing(self):
        """Test checking specific missing dependency."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            from provide.foundation.cli.commands.deps import deps_command
            
            with patch('provide.foundation.utils.deps.has_dependency', return_value=False):
                with patch('builtins.print') as mock_print:
                    with pytest.raises(SystemExit) as exc_info:
                        deps_command.callback(quiet=False, check='crypto')
                    
                    assert exc_info.value.code == 1
                    assert mock_print.call_count == 2
                    mock_print.assert_any_call("❌ crypto: Missing")
                    mock_print.assert_any_call("Install with: pip install 'provide-foundation[crypto]'")
    
    def test_deps_command_check_specific_quiet(self):
        """Test checking specific dependency in quiet mode."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            from provide.foundation.cli.commands.deps import deps_command
            
            with patch('provide.foundation.utils.deps.has_dependency', return_value=True):
                with patch('builtins.print') as mock_print:
                    with pytest.raises(SystemExit) as exc_info:
                        deps_command.callback(quiet=True, check='cli')
                    
                    assert exc_info.value.code == 0
                    mock_print.assert_not_called()
    
    def test_deps_command_check_all_available(self):
        """Test checking all dependencies when all available."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            from provide.foundation.cli.commands.deps import deps_command
            
            mock_dep = Mock(available=True)
            with patch('provide.foundation.utils.deps.check_optional_deps', 
                      return_value=[mock_dep, mock_dep]):
                with pytest.raises(SystemExit) as exc_info:
                    deps_command.callback(quiet=False, check=None)
                
                assert exc_info.value.code == 0
    
    def test_deps_command_check_all_some_missing(self):
        """Test checking all dependencies when some missing."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            from provide.foundation.cli.commands.deps import deps_command
            
            mock_dep_available = Mock(available=True)
            mock_dep_missing = Mock(available=False)
            with patch('provide.foundation.utils.deps.check_optional_deps', 
                      return_value=[mock_dep_available, mock_dep_missing]):
                with pytest.raises(SystemExit) as exc_info:
                    deps_command.callback(quiet=False, check=None)
                
                assert exc_info.value.code == 1
    
    def test_deps_command_check_all_quiet(self):
        """Test checking all dependencies in quiet mode."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            from provide.foundation.cli.commands.deps import deps_command
            
            mock_dep = Mock(available=True)
            with patch('provide.foundation.utils.deps.check_optional_deps', 
                      return_value=[mock_dep]) as mock_check:
                with pytest.raises(SystemExit) as exc_info:
                    deps_command.callback(quiet=True, check=None)
                
                assert exc_info.value.code == 0
                mock_check.assert_called_once_with(quiet=True, return_status=True)


class TestDepsCommandWithoutClick:
    """Test deps command when click is not available."""
    
    def test_deps_command_without_click(self):
        """Test deps_command raises error when click not available."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', False):
            # Need to reload the module to get the stub version
            import importlib
            import provide.foundation.cli.commands.deps as deps_module
            importlib.reload(deps_module)
            
            with pytest.raises(ImportError, match="CLI commands require optional dependencies"):
                deps_module.deps_command()
    
    def test_require_click_raises_error(self):
        """Test _require_click raises appropriate error."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', False):
            from provide.foundation.cli.commands.deps import _require_click
            
            with pytest.raises(ImportError) as exc_info:
                _require_click()
            
            assert "CLI commands require optional dependencies" in str(exc_info.value)
            assert "pip install 'provide-foundation[cli]'" in str(exc_info.value)
    
    def test_deps_command_stub_with_args(self):
        """Test deps_command stub ignores args and raises error."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', False):
            import importlib
            import provide.foundation.cli.commands.deps as deps_module
            importlib.reload(deps_module)
            
            with pytest.raises(ImportError, match="CLI commands require optional dependencies"):
                deps_module.deps_command("arg1", kwarg1="value1")


class TestDepsCommandDecorators:
    """Test click decorators on deps_command."""
    
    def test_click_decorators_applied(self):
        """Test that click decorators are properly applied."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            with patch('provide.foundation.cli.commands.deps.click') as mock_click:
                # Set up mock decorators
                mock_click.command = Mock(return_value=lambda f: f)
                mock_click.option = Mock(return_value=lambda f: f)
                
                # Reload module to apply decorators
                import importlib
                import provide.foundation.cli.commands.deps as deps_module
                importlib.reload(deps_module)
                
                # Verify decorators were called
                mock_click.command.assert_called_once_with("deps")
                assert mock_click.option.call_count == 2
                
                # Check option configurations
                option_calls = mock_click.option.call_args_list
                # First option: --quiet
                assert option_calls[0].kwargs['is_flag'] is True
                assert option_calls[0].kwargs['help'] == "Suppress output, just return exit code"
                # Second option: --check
                assert option_calls[1].kwargs['metavar'] == "DEPENDENCY"
                assert option_calls[1].kwargs['help'] == "Check specific dependency only"


class TestDepsCommandModuleImport:
    """Test module-level import behavior."""
    
    def test_module_imports_successfully(self):
        """Test module imports without errors."""
        import provide.foundation.cli.commands.deps
        assert provide.foundation.cli.commands.deps.__all__ == ["deps_command"]
    
    def test_has_click_flag_exists(self):
        """Test _HAS_CLICK flag exists."""
        from provide.foundation.cli.commands import deps
        assert hasattr(deps, '_HAS_CLICK')
        assert isinstance(deps._HAS_CLICK, bool)
    
    def test_click_import_handling(self):
        """Test click import is handled properly."""
        # Remove click from sys.modules temporarily
        click_module = sys.modules.pop('click', None)
        try:
            # Reload without click
            import importlib
            import provide.foundation.cli.commands.deps as deps_module
            importlib.reload(deps_module)
            assert deps_module._HAS_CLICK is False
            assert deps_module.click is None
        finally:
            # Restore click if it was there
            if click_module:
                sys.modules['click'] = click_module
                importlib.reload(deps_module)


class TestDepsCommandEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_deps_list(self):
        """Test handling empty dependency list."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            from provide.foundation.cli.commands.deps import deps_command
            
            with patch('provide.foundation.utils.deps.check_optional_deps', return_value=[]):
                with pytest.raises(SystemExit) as exc_info:
                    deps_command.callback(quiet=False, check=None)
                
                assert exc_info.value.code == 0  # No deps means all available
    
    def test_check_nonexistent_dependency(self):
        """Test checking non-existent dependency."""
        with patch('provide.foundation.cli.commands.deps._HAS_CLICK', True):
            from provide.foundation.cli.commands.deps import deps_command
            
            with patch('provide.foundation.utils.deps.has_dependency', return_value=False):
                with patch('builtins.print'):
                    with pytest.raises(SystemExit) as exc_info:
                        deps_command.callback(quiet=False, check='nonexistent')
                    
                    assert exc_info.value.code == 1