#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Version consistency checker for Foundation Telemetry.

This script ensures that version numbers are consistent across the project
and that the dynamic versioning system works correctly.

The checker validates:
- Version format compliance with semantic versioning
- Dynamic versioning system functionality
- Version consistency across project files
- Git tag alignment (if in a git repository)
- Changelog entries for current version

This tool is designed to be run as part of CI/CD pipelines and pre-commit
hooks to catch version-related issues early in the development process."""

from pathlib import Path
import sys
import tomllib


def load_pyproject_version() -> str:
    """Load version from pyproject.toml or VERSION file for dynamic versioning.

    This function reads the project configuration file and extracts
    the version string for validation against other version sources.
    Handles both static and dynamic versioning.

    Returns:
        The version string from pyproject.toml or VERSION file.

    Raises:
        FileNotFoundError: If pyproject.toml is not found.
        ValueError: If no version is found in the configuration.

    """
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")

    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)

    # Check for static version first
    version = data.get("project", {}).get("version")

    # If no static version, check for dynamic versioning
    if not version:
        dynamic_fields = data.get("project", {}).get("dynamic", [])
        if "version" in dynamic_fields:
            # Check for setuptools dynamic version configuration
            dynamic_config = data.get("tool", {}).get("setuptools", {}).get("dynamic", {})
            version_config = dynamic_config.get("version", {})

            if "file" in version_config:
                version_file = Path(version_config["file"])
                if version_file.exists():
                    version = version_file.read_text().strip()
                else:
                    raise FileNotFoundError(f"Version file {version_file} not found")
            else:
                raise ValueError("Dynamic version configured but no file specified")
        else:
            raise ValueError("No version found in pyproject.toml")

    return version


def check_dynamic_versioning() -> str:
    """Test the dynamic versioning system.

    This function validates that the package's dynamic versioning
    mechanism works correctly by importing the package and checking
    the __version__ attribute.

    Returns:
        The version string returned by dynamic versioning.

    Raises:
        ImportError: If the package cannot be imported.
        RuntimeError: If dynamic versioning fails.

    """
    # Add src to path for importing during development
    src_path = Path("src")
    if src_path.exists():
        sys.path.insert(0, str(src_path))

    try:
        # Import and check if versioning works
        from provide.foundation import __version__

        match __version__:
            case "0.0.0-dev":
                print(
                    "ℹ️  Using development fallback version (expected in dev environment)",
                )
                return __version__
            case version_str if version_str:
                print(f"✅ Dynamic versioning working: {version_str}")
                return version_str
            case _:
                raise ValueError("Dynamic versioning returned empty version")

    except ImportError as e:
        raise ImportError(f"Failed to import provide.foundation: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Dynamic versioning failed: {e}") from e


def validate_version_format(version: str) -> bool:
    """Validate that version follows semantic versioning.

    This function checks that the version string conforms to semantic
    versioning standards, ensuring consistency and compatibility with
    packaging tools.

    Args:
        version: The version string to validate.

    Returns:
        True if the version format is valid, False otherwise.

    Example:
        >>> validate_version_format("1.0.0")
        True
        >>> validate_version_format("1.0.0-rc1")
        True
        >>> validate_version_format("invalid")
        False

    """
    import re

    # Basic semantic versioning pattern
    # Allows: 1.0.0, 1.0.0-rc1, 1.0.0-beta.1, 1.0.0+build.1
    # Also allows dev versions: 0.0.0.dev0, 0.0.0.dev2, etc.
    pattern = r"^(\d+)\.(\d+)\.(\d+)(\.dev\d+)?(?:-([a-zA-Z0-9\-\.]+))?(?:\+([a-zA-Z0-9\-\.]+))?$"

    if not re.match(pattern, version):
        return False

    # Additional validation for numeric components
    parts = version.split("-")[0].split(".")
    try:
        major, minor, patch = map(int, parts[:3])
        return major >= 0 and minor >= 0 and patch >= 0
    except (ValueError, IndexError):
        return False


def check_changelog_mentions_version(version: str) -> bool:
    """Check if the current version is mentioned in CHANGELOG.md.

    This function searches for version entries in the changelog to ensure
    that releases are properly documented.

    Args:
        version: The version string to search for.

    Returns:
        True if the version is found in the changelog, False otherwise.

    """
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        print("⚠️  CHANGELOG.md not found - skipping changelog check")
        return True

    with changelog_path.open("r", encoding="utf-8") as f:
        content = f.read()

    # Look for version in changelog (various formats)
    version_patterns = [
        f"[{version}]",
        f"## [{version}]",
        f"# {version}",
        f"## {version}",
        version,
    ]

    return any(pattern in content for pattern in version_patterns)


def check_git_tag_consistency(version: str) -> bool:
    """Check if current version matches latest git tag (if in git repo).

    This function validates that git tags are consistent with the
    project version, which is important for release automation.

    Args:
        version: The version string to check against git tags.

    Returns:
        True if git tag is consistent or if git is unavailable.

    """
    try:
        import subprocess

        # Get latest git tag for current commit
        result = subprocess.run(
            ["git", "describe", "--tags", "--exact-match", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )

        match result.returncode:
            case 0:
                latest_tag = result.stdout.strip()
                expected_tag = f"v{version}"

                if latest_tag == expected_tag:
                    print(f"✅ Git tag matches version: {latest_tag}")
                    return True
                print(f"⚠️  Git tag mismatch: tag={latest_tag}, version=v{version}")
                return False
            case _:
                print("ℹ️  No exact git tag for current commit (normal for development)")
                return True

    except FileNotFoundError:
        print("ℹ️  Git not available - skipping tag check")
        return True
    except Exception as e:
        print(f"⚠️  Git tag check failed: {e}")
        return True  # Don't fail on git issues


def main() -> None:
    """Run all version consistency checks.

    This function orchestrates all version validation checks and reports
    the results. It's designed to be used in CI/CD pipelines and returns
    appropriate exit codes for automation.
    """
    print("🔍 Checking version consistency...")
    print("=" * 50)

    success = True

    try:
        # 1. Load pyproject.toml version
        pyproject_version = load_pyproject_version()
        print(f"📋 pyproject.toml version: {pyproject_version}")

        # 2. Validate version format
        if not validate_version_format(pyproject_version):
            print(f"❌ Invalid version format: {pyproject_version}")
            print("   Expected semantic versioning (e.g., 1.0.0, 1.0.0-rc1)")
            success = False
        else:
            print(f"✅ Version format valid: {pyproject_version}")

        # 3. Test dynamic versioning
        try:
            dynamic_version = check_dynamic_versioning()

            # Handle development environment case
            match dynamic_version:
                case "0.0.0-dev":
                    print("ℹ️  Development environment detected")
                case version if version != pyproject_version:
                    print("❌ Version mismatch!")
                    print(f"   pyproject.toml: {pyproject_version}")
                    print(f"   dynamic import: {version}")
                    print(
                        "   This suggests the package isn't installed in development mode",
                    )
                    success = False
                case _:
                    print(f"✅ Dynamic versioning matches: {dynamic_version}")

        except Exception as e:
            print(f"❌ Dynamic versioning failed: {e}")
            success = False

        # 4. Check changelog
        if not check_changelog_mentions_version(pyproject_version):
            print(f"⚠️  Version {pyproject_version} not found in CHANGELOG.md")
            print("   Consider adding an entry for this version")
            # Don't fail for this - it's just a warning
        else:
            print("✅ Version found in CHANGELOG.md")

        # 5. Check git tag consistency (if applicable)
        check_git_tag_consistency(pyproject_version)

        print("=" * 50)

        match success:
            case True:
                print("✅ All version consistency checks passed!")
                sys.exit(0)
            case False:
                print("❌ Version consistency issues found!")
                sys.exit(1)

    except Exception as e:
        print(f"💥 Version check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# 🔍📋

# 🧱🏗️🔚
