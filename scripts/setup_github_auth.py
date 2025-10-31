#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""GitHub Organization Helper Token Setup.

Configures git authentication for private repositories across organizations
using helper tokens stored in GH_ORG_HELPERS environment variable."""

from __future__ import annotations

import json
import os
import subprocess
import sys


def setup_git_auth() -> None:
    """Configure git authentication using organization helper tokens."""
    helpers_json = os.environ.get("GH_ORG_HELPERS")

    if not helpers_json:
        print("No GH_ORG_HELPERS found - using public access only")
        return

    try:
        helpers: dict[str, str] = json.loads(helpers_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing GH_ORG_HELPERS JSON: {e}", file=sys.stderr)
        sys.exit(1)

    configured_orgs = []

    for org, token in helpers.items():
        if not token.startswith(("ghp_", "github_pat_")):
            print(f"Warning: Token for {org} doesn't look like a GitHub PAT", file=sys.stderr)

        # Configure git to use token for this organization
        git_url = f"https://{token}@github.com/{org}/"
        insteadof_url = f"https://github.com/{org}/"

        try:
            subprocess.run(
                ["git", "config", "--global", f"url.{git_url}.insteadOf", insteadof_url],
                check=True,
                capture_output=True,
            )

            configured_orgs.append(org)

        except subprocess.CalledProcessError as e:
            print(f"Failed to configure git for {org}: {e}", file=sys.stderr)
            sys.exit(1)

    if configured_orgs:
        print(f"Configured GitHub auth for organizations: {', '.join(configured_orgs)}")
    else:
        print("No organizations configured for GitHub auth")


def main() -> None:
    """Main entry point."""
    setup_git_auth()


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
