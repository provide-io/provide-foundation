# Testing GitHub Workflows Locally with act

This guide explains how to test the provide-foundation GitHub Actions workflows locally using [act](https://github.com/nektos/act).

## What is act?

`act` is a tool that allows you to run GitHub Actions locally. It uses Docker to pull images and run your workflows in containers that simulate the GitHub Actions environment.

## Installation

### macOS
```bash
brew install act
```

### Linux
```bash
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Windows
```bash
choco install act-cli
# or
scoop install act
```

### Docker Requirement
⚠️ **Important**: act requires Docker to be installed and running:
```bash
# Check if Docker is running
docker version

# If not installed, get it from:
# https://www.docker.com/get-started
```

## Configuration

The project includes an `.actrc` configuration file that sets up act with appropriate defaults.

### Setting Up Secrets

1. Copy the example secrets file:
```bash
cp .secrets.example .secrets
```

2. Edit `.secrets` and add your tokens:
```bash
# Edit with your preferred editor
vim .secrets
# or
nano .secrets
```

3. Add to `.gitignore` (already included):
```bash
echo ".secrets" >> .gitignore
```

## Running Workflows

### Basic Commands

```bash
# List available workflows
act -l

# Run the default push event
act

# Run a specific event
act push
act pull_request
act workflow_dispatch

# Run a specific workflow
act -W .github/workflows/ci.yml

# Run a specific job
act -j test

# Dry run (show what would be executed)
act -n
```

### Testing CI Workflow

```bash
# Run full CI pipeline
act push -W .github/workflows/ci.yml

# Run only tests
act push -W .github/workflows/ci.yml -j test

# Run with specific Python version
act push -W .github/workflows/ci.yml --matrix python-version:3.11

# Run with verbose output
act push -W .github/workflows/ci.yml --verbose
```

### Testing Documentation Workflow

```bash
# Run docs validation
act push -W .github/workflows/docs.yml

# Simulate a PR with doc changes
act pull_request -W .github/workflows/docs.yml
```

### Testing Release Workflow

```bash
# Test release build (without deployment)
act workflow_dispatch -W .github/workflows/release.yml \
  -s PYPI_API_TOKEN=fake-token \
  -s TEST_PYPI_API_TOKEN=fake-token

# Simulate tag push
act push -W .github/workflows/release.yml --eventpath event.json
```

Create `event.json` for tag simulation:
```json
{
  "ref": "refs/tags/v1.0.0",
  "ref_type": "tag"
}
```

## Workflow Compatibility

### ✅ Fully Supported Workflows

| Workflow | Command | Notes |
|----------|---------|-------|
| CI - Quality Checks | `act -W .github/workflows/ci.yml -j quality` | Runs linting and type checking |
| CI - Tests | `act -W .github/workflows/ci.yml -j test` | Runs test suite |
| CI - Package Build | `act -W .github/workflows/ci.yml -j package` | Builds packages |
| Documentation | `act -W .github/workflows/docs.yml` | Validates docs |

### ⚠️ Partially Supported

| Workflow | Limitations | Workaround |
|----------|------------|------------|
| CI - macOS Tests | act doesn't support macOS runners | Tests run on Linux container |
| Release - PyPI Deploy | Can't actually deploy | Use `--dry-run` flag or mock tokens |
| Integration Tests | May need local services | Use Docker Compose for dependencies |

### ❌ Not Supported

| Feature | Reason | Alternative |
|---------|--------|-------------|
| macOS/Windows runners | act only supports Linux containers | Test on Linux or use CI |
| GitHub Environments | No environment protection rules | Test with different secret sets |
| Codecov Upload | Requires real token and network | Use fake token for testing |
| GitHub Release Creation | Requires GitHub API access | Test locally with `--dry-run` |

## Common Use Cases

### 1. Pre-Push Testing
```bash
# Run before pushing to catch issues early
act push -j quality
act push -j test --matrix python-version:3.11
```

### 2. PR Validation
```bash
# Test how PR checks will run
act pull_request
```

### 3. Release Testing
```bash
# Test release build without deployment
act workflow_dispatch -W .github/workflows/release.yml \
  --input deploy_target=none
```

### 4. Debugging Workflow Issues
```bash
# Run with shell access for debugging
act push -j test --container-options "--entrypoint /bin/bash"

# Very verbose output
act push --verbose --verbose
```

## Advanced Configuration

### Custom Runner Images

For better compatibility with GitHub Actions:

```bash
# Use larger images that more closely match GitHub
act --platform ubuntu-latest=catthehacker/ubuntu:full-latest

# Use specific Ubuntu version
act --platform ubuntu-22.04=catthehacker/ubuntu:full-22.04
```

### Resource Limits

```bash
# Limit CPU and memory
act --container-options "--cpus=2 --memory=4g"
```

### Matrix Testing

```bash
# Test specific matrix combinations
act push -W .github/workflows/ci.yml \
  --matrix os:ubuntu-latest \
  --matrix python-version:3.11

# Test all matrix combinations
act push -W .github/workflows/ci.yml --matrix os:ubuntu-latest
```

### Using Docker Compose

For complex workflows with services:

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: test
    ports:
      - 5432:5432
  
  redis:
    image: redis:7
    ports:
      - 6379:6379
```

```bash
# Start services
docker-compose -f docker-compose.test.yml up -d

# Run tests
act push -j integration

# Clean up
docker-compose -f docker-compose.test.yml down
```

## Troubleshooting

### Issue: Docker not running
```bash
# Start Docker
open -a Docker  # macOS
sudo systemctl start docker  # Linux
```

### Issue: Rate limiting on Docker Hub
```bash
# Login to Docker Hub
docker login

# Or use GitHub Container Registry images
act --platform ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest
```

### Issue: Workflow fails locally but works on GitHub
```bash
# Try with larger runner image
act --platform ubuntu-latest=catthehacker/ubuntu:full-latest

# Check for GitHub-specific features
act --env GITHUB_ACTIONS=true
```

### Issue: Secrets not working
```bash
# Verify secrets file
cat .secrets

# Pass secrets explicitly
act push -s MY_SECRET=value

# Use environment variables
export MY_SECRET=value
act push --env-file .env
```

### Issue: Can't find workflow
```bash
# List all workflows
find .github/workflows -name "*.yml" -o -name "*.yaml"

# Specify exact path
act -W .github/workflows/ci.yml
```

## Performance Tips

1. **Use --reuse flag**: Reuses containers between runs
   ```bash
   act push --reuse
   ```

2. **Cache Docker images**: Pull images beforehand
   ```bash
   docker pull catthehacker/ubuntu:act-latest
   ```

3. **Run specific jobs**: Don't run entire workflows
   ```bash
   act -j specific-job
   ```

4. **Use smaller images for simple tests**:
   ```bash
   act --platform ubuntu-latest=node:16-slim
   ```

## Limitations to Remember

1. **No macOS/Windows support**: Only Linux containers
2. **No GitHub API**: Can't create releases, comments, etc.
3. **No built-in services**: Need to run databases separately
4. **Different environment**: Some GitHub-specific features unavailable
5. **Performance**: Slower than GitHub's runners

## Best Practices

1. **Keep a .secrets.example file**: Help others set up quickly
2. **Use act for pre-push validation**: Catch issues early
3. **Don't rely solely on act**: Always verify on real GitHub Actions
4. **Use --dry-run for dangerous operations**: Prevent accidents
5. **Document act-specific workarounds**: In your workflow files

## Example Workflow Testing Script

Create `test-workflows.sh`:

```bash
#!/bin/bash
set -e

echo "🧪 Testing GitHub Workflows with act"

# Check Docker
if ! docker version > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

# Check act
if ! command -v act > /dev/null 2>&1; then
    echo "❌ act is not installed"
    exit 1
fi

# Setup secrets if needed
if [ ! -f .secrets ]; then
    cp .secrets.example .secrets
    echo "⚠️  Created .secrets file - please add your tokens"
fi

echo "✅ Running quality checks..."
act -j quality || echo "⚠️  Quality checks failed"

echo "✅ Running tests..."
act -j test --matrix python-version:3.11 || echo "⚠️  Tests failed"

echo "✅ Testing package build..."
act -j package || echo "⚠️  Package build failed"

echo "✅ Testing documentation..."
act -W .github/workflows/docs.yml || echo "⚠️  Documentation check failed"

echo "✨ Workflow testing complete!"
```

Make it executable:
```bash
chmod +x test-workflows.sh
./test-workflows.sh
```

## Conclusion

While act can't perfectly replicate the GitHub Actions environment, it's excellent for:
- Quick validation of workflow syntax
- Testing job logic locally
- Debugging workflow issues
- Pre-push validation

Always do final testing on actual GitHub Actions, but use act to speed up your development cycle!