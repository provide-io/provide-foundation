class TestGetStr(FoundationTestCase):
    """Test get_str method."""

    def test_get_str_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing string variable."""
        os.environ["APP_NAME"] = "myapp"
        env = EnvPrefix("app")
        assert env.get_str("name") == "myapp"

    def test_get_str_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        assert env.get_str("name", default="default") == "default"

    def test_get_str_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_str("name") is None


class TestGetPath(FoundationTestCase):
    """Test get_path method."""

    def test_get_path_existing_variable(self, clean_env: Any) -> None:
        """Test getting existing path variable."""
        os.environ["APP_CONFIG_PATH"] = "/etc/app/config"
        env = EnvPrefix("app")
        result = env.get_path("config_path")
        assert result == Path("/etc/app/config")

    def test_get_path_missing_variable_with_default(self, clean_env: Any) -> None:
        """Test getting missing variable with default."""
        env = EnvPrefix("app")
        default_path = Path("/default/path")
        result = env.get_path("config_path", default=default_path)
        assert result == default_path

    def test_get_path_missing_variable_no_default(self, clean_env: Any) -> None:
        """Test getting missing variable without default."""
        env = EnvPrefix("app")
        assert env.get_path("config_path") is None

    def test_get_path_with_string_default(self, clean_env: Any) -> None:
        """Test getting path with string default."""
        env = EnvPrefix("app")
        result = env.get_path("config_path", default="/default/path")
        assert result == Path("/default/path")
