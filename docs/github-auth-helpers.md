# GitHub Organization Helper Tokens

This document explains how to use organization helper tokens to access private repositories across GitHub organizations in CI/CD pipelines.

## Overview

The helper token system allows your GitHub Actions workflows to securely access private repositories from different organizations without exposing organization names or token details in workflow files.

## Setup

### 1. Create Personal Access Tokens

Create GitHub Personal Access Tokens (PATs) for each organization you need access to:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Create a token with repository access for the target organization
3. Grant necessary permissions (typically `Contents: Read` and `Metadata: Read`)

### 2. Configure Repository Secret

Add a repository secret named `GH_ORG_HELPERS` containing a JSON mapping of organizations to tokens:

```json
{
  "livingstaccato": "ghp_xxxxxxxxxxxxxxxxxxxxx",
  "another-org": "github_pat_yyyyyyyyyyyyy"
}
```

**Important**: Use the exact organization name as it appears in GitHub URLs.

## Usage in GitHub Actions

### Method 1: Using the Composite Action

```yaml
name: CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup GitHub Auth
        uses: ./.github/actions/setup-auth
        with:
          helpers-json: ${{ secrets.GH_ORG_HELPERS }}

      - name: Install Dependencies
        run: uv sync  # Can now access private repos
```

### Method 2: Direct Script Usage

```yaml
- name: Setup GitHub Auth
  env:
    GH_ORG_HELPERS: ${{ secrets.GH_ORG_HELPERS }}
  run: python3 scripts/setup_github_auth.py

- name: Install Dependencies
  run: uv sync
```

## Local Development

For local development, set the environment variable:

```bash
export GH_ORG_HELPERS='{"livingstaccato": "ghp_your_token_here"}'
python3 scripts/setup_github_auth.py
```

## How It Works

The system configures git URL rewriting to automatically use helper tokens:

1. Reads the `GH_ORG_HELPERS` environment variable
2. Parses the JSON mapping of organizations to tokens
3. Configures git to rewrite URLs like:
   - `https://github.com/livingstaccato/repo` → `https://token@github.com/livingstaccato/repo`

## Security Considerations

- **Token Scope**: Use fine-grained tokens with minimal necessary permissions
- **Token Rotation**: Regularly rotate helper tokens
- **Organization Privacy**: Organization names remain private (not exposed in workflow files)
- **Secret Management**: Only store tokens in GitHub Secrets, never in code

## Troubleshooting

### "Authentication failed" errors
- Verify the token has correct permissions for the repository
- Check that the organization name in the JSON matches exactly
- Ensure the token hasn't expired

### "No GH_ORG_HELPERS found" message
- This is normal for public-only repositories
- The system gracefully falls back to public access

### Git configuration issues
- The script configures global git settings
- Multiple runs will override previous configurations
- Local development may persist git config between runs

## Example Project Structure

```
my-project/
├── .github/
│   ├── actions/
│   │   └── setup-auth/
│   │       └── action.yml
│   └── workflows/
│       └── ci.yml
├── scripts/
│   └── setup_github_auth.py
└── pyproject.toml  # Contains git+https:// dependencies
```

## Migration from Individual Tokens

If you're currently using individual `GH_ORG_HELPER_*` secrets, migrate to the JSON format:

**Old (multiple secrets):**
```
GH_ORG_HELPER_LIVINGSTACCATO = "ghp_xxx"
GH_ORG_HELPER_ANOTHER_ORG = "ghp_yyy"
```

**New (single JSON secret):**
```json
{
  "livingstaccato": "ghp_xxx",
  "another-org": "ghp_yyy"
}
```

This approach is more maintainable and keeps organization relationships private.