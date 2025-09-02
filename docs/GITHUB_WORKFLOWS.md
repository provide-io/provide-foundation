# GitHub Workflows Configuration

This document describes the GitHub Actions workflows and required secrets for the provide-foundation project.

## Workflows Overview

The project uses 5 GitHub Actions workflows:

1. **CI - Tests & Quality** (`.github/workflows/ci.yml`)
   - Runs on push/PR to main and develop branches
   - Executes code quality checks, tests, and package building
   - Tests across Python 3.11, 3.12, and 3.13 on Ubuntu and macOS

2. **Documentation** (`.github/workflows/docs.yml`)
   - Validates documentation changes
   - Tests example scripts
   - Validates README links

3. **Release & Deployment** (`.github/workflows/release.yml`)
   - Triggered on version tags (v*) or manual dispatch
   - Builds and publishes packages to PyPI/Test PyPI
   - Creates GitHub releases

4. **Performance** (`.github/workflows/performance.yml`)
   - Runs performance benchmarks
   - Tracks performance metrics over time

5. **Security** (`.github/workflows/security.yml`)
   - Security scanning and vulnerability checks

## Required Secrets

To enable full workflow functionality, configure these secrets in your GitHub repository settings:

### Essential Secrets

| Secret Name | Description | Required For | How to Obtain |
|------------|-------------|--------------|---------------|
| `CODECOV_TOKEN` | Codecov integration token | CI workflow - coverage reporting | [codecov.io](https://codecov.io) → Settings → Repository Upload Token |
| `PYPI_API_TOKEN` | PyPI publishing token | Release workflow - production deployment | [pypi.org](https://pypi.org) → Account Settings → API Tokens → Add Token (scope: project) |
| `TEST_PYPI_API_TOKEN` | Test PyPI publishing token | Release workflow - test deployment | [test.pypi.org](https://test.pypi.org) → Account Settings → API Tokens |

### Optional Secrets

| Secret Name | Description | Used For |
|------------|-------------|----------|
| `SLACK_WEBHOOK_URL` | Slack notifications | Build status notifications |
| `SONAR_TOKEN` | SonarCloud token | Code quality analysis |

## Setting Up Secrets

### 1. Navigate to Repository Settings
```
https://github.com/provide-io/provide-foundation/settings/secrets/actions
```

### 2. Add Required Secrets

#### CODECOV_TOKEN
1. Sign up or log in to [Codecov](https://codecov.io)
2. Add your repository
3. Copy the upload token
4. Add as `CODECOV_TOKEN` secret

#### PYPI_API_TOKEN
1. Log in to [PyPI](https://pypi.org)
2. Go to Account Settings → API tokens
3. Create a new token:
   - Name: `provide-foundation-github`
   - Scope: Project (provide-foundation)
4. Copy the token (starts with `pypi-`)
5. Add as `PYPI_API_TOKEN` secret

#### TEST_PYPI_API_TOKEN
1. Log in to [Test PyPI](https://test.pypi.org)
2. Follow same steps as PyPI
3. Add as `TEST_PYPI_API_TOKEN` secret

## Workflow Configuration

### CI Workflow

The CI workflow runs automatically on:
- Push to `main` or `develop` branches
- Pull requests targeting these branches
- Manual workflow dispatch

**Key Jobs:**
- `quality`: Linting and type checking
- `test`: Test matrix across OS and Python versions
- `package`: Build and validate packages
- `integration`: Integration test suite

### Release Workflow

The release workflow supports:
- Automatic deployment on version tags (`v*`)
- Manual deployment with target selection
- Force deployment option (bypasses validation)

**Deployment Targets:**
- `none`: Build only, no deployment
- `test-pypi`: Deploy to Test PyPI
- `pypi`: Deploy to production PyPI

### Manual Workflow Dispatch

To manually trigger a release:

1. Go to Actions → Release & Deployment
2. Click "Run workflow"
3. Select:
   - Branch/tag to deploy
   - Deployment target
   - Force deploy option (if needed)

## Environment Configuration

The workflows use GitHub Environments for deployment protection:

### test-pypi Environment
- Used for Test PyPI deployments
- No approval required
- Add `TEST_PYPI_API_TOKEN` secret

### pypi Environment
- Used for production PyPI deployments
- Consider adding:
  - Required reviewers
  - Deployment branch restrictions
  - Wait timer

## Workflow Fixes Applied

The following issues have been fixed in the workflows:

1. **Python Setup**: Added missing `python-version` parameter to all Python setup steps
2. **UV Version**: Updated to v4 for consistency
3. **Coverage File**: Fixed coverage file path from `test-results.xml` to `coverage.xml`
4. **Job Configuration**: Added missing `runs-on` for jobs with matrix strategy
5. **Version Variables**: Fixed `${{ env.PYTHON_VERSION }}` to use `${{ matrix.python-version }}`

## Testing Workflows Locally

You can test workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux

# Test CI workflow
act push

# Test release workflow
act workflow_dispatch -W .github/workflows/release.yml

# With secrets (create .secrets file)
act push --secret-file .secrets
```

## Monitoring Workflow Status

### Badges

Add these badges to your README:

```markdown
[![CI](https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml/badge.svg)](https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/provide-io/provide-foundation/branch/main/graph/badge.svg)](https://codecov.io/gh/provide-io/provide-foundation)
[![PyPI version](https://badge.fury.io/py/provide-foundation.svg)](https://badge.fury.io/py/provide-foundation)
```

### Workflow Notifications

Configure notifications in `.github/workflows/ci.yml`:

```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "Build failed on ${{ github.ref }}",
        "blocks": [{
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "Build failed: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
          }
        }]
      }
```

## Troubleshooting

### Common Issues

1. **Codecov upload fails**
   - Verify `CODECOV_TOKEN` is set correctly
   - Check if repository is activated on Codecov

2. **PyPI deployment fails**
   - Ensure package version is unique
   - Verify API token has correct scope
   - Check if package name is available

3. **Test failures on specific Python version**
   - Review version-specific dependencies
   - Check for deprecated features

4. **Workflow doesn't trigger**
   - Verify branch protection rules
   - Check workflow file syntax
   - Ensure proper permissions

### Debug Mode

Enable debug logging for workflows:

1. Go to Settings → Secrets → Actions
2. Add repository secret:
   - Name: `ACTIONS_RUNNER_DEBUG`
   - Value: `true`

## Maintenance

### Updating Dependencies

The workflows use pinned versions for stability:

- UV Package Manager: `0.7.8`
- Python versions: `3.11`, `3.12`, `3.13`
- Actions versions: Check for updates quarterly

### Security

- Regularly rotate API tokens
- Use environment protection rules
- Enable required status checks
- Configure branch protection

## Contact

For workflow issues or questions:
- Open an issue on [GitHub](https://github.com/provide-io/provide-foundation/issues)
- Check [Actions tab](https://github.com/provide-io/provide-foundation/actions) for logs