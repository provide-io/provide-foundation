# Testing GitHub Actions with act and Colima

This guide explains how to test GitHub Actions workflows locally using [act](https://github.com/nektos/act) with [Colima](https://github.com/abiosoft/colima) as the Docker runtime on macOS.

## Prerequisites

1. **Colima** - Docker runtime for macOS
   ```bash
   brew install colima
   colima start
   ```

2. **act** - Local GitHub Actions runner
   ```bash
   brew install act
   ```

3. **Docker CLI**
   ```bash
   brew install docker
   ```

## Known Issue: Docker Socket Mounting

When using act with Colima, you may encounter an error:
```
error while creating mount source path '/Users/tim/.colima/default/docker.sock': mkdir /Users/tim/.colima/default/docker.sock: operation not supported
```

This happens because act tries to mount the Docker socket into containers, but Colima's virtualization layer doesn't support this operation. The solution is to disable socket mounting using the `--container-daemon-socket -` flag.

## Solution

### Method 1: Use the Provided Script (Recommended)

Use the `act-colima.sh` wrapper script that handles the configuration automatically:

```bash
# Test a specific workflow
./act-colima.sh -W .github/workflows/test-simple.yml

# Run the default CI workflow
./act-colima.sh

# Run a specific job
./act-colima.sh -j test

# List available workflows
./act-colima.sh -l
```

### Method 2: Manual Configuration

Set the Docker host and disable socket mounting:

```bash
# Set Docker host to Colima's socket
export DOCKER_HOST="unix:///Users/tim/.colima/default/docker.sock"

# Run act with disabled socket mounting
act --container-daemon-socket "" -W .github/workflows/test-simple.yml
```

### Method 3: Create an Alias

Add this to your shell configuration (`~/.bashrc` or `~/.zshrc`):

```bash
alias act='DOCKER_HOST="unix:///Users/tim/.colima/default/docker.sock" act --container-daemon-socket ""'
```

## Configuration Files

### `.actrc`
The project includes an `.actrc` file with optimized settings for running workflows:

```ini
# Runner image mappings
-P ubuntu-latest=catthehacker/ubuntu:act-latest
-P ubuntu-22.04=catthehacker/ubuntu:act-22.04
-P ubuntu-20.04=catthehacker/ubuntu:act-20.04

# Use local secrets file
--secret-file .secrets

# Architecture for Apple Silicon
--container-architecture linux/amd64

# Reuse containers for speed
--reuse
```

### `.secrets`
Create a `.secrets` file for workflow secrets (already in `.gitignore`):

```bash
cp .secrets.example .secrets
# Edit .secrets with your actual tokens if needed
```

For testing, placeholder values are sufficient:
```
CODECOV_TOKEN=test-codecov-token
PYPI_API_TOKEN=pypi-test-token
TEST_PYPI_API_TOKEN=pypi-test-token
GITHUB_TOKEN=test-github-token
```

## Running Tests

### Test Simple Workflow
```bash
./act-colima.sh -W .github/workflows/test-simple.yml
```

### Run CI Tests
```bash
# Run all test jobs
./act-colima.sh -W .github/workflows/ci.yml

# Run specific test matrix
./act-colima.sh -W .github/workflows/ci.yml -j test
```

### Run Linting and Quality Checks
```bash
./act-colima.sh -W .github/workflows/ci.yml -j quality
```

### Test Documentation Build
```bash
./act-colima.sh -W .github/workflows/docs.yml
```

## Troubleshooting

### Docker not running
```bash
# Check Colima status
colima status

# Start Colima if needed
colima start
```

### Verify Docker connection
```bash
# Should show Colima as the context
docker context ls

# Test Docker
docker ps
```

### Socket issues persist

If you still see socket-related errors:

1. Ensure no symlinks exist at `~/.colima/docker.sock`:
   ```bash
   rm -f ~/.colima/docker.sock
   ```

2. Check your Docker host is set correctly:
   ```bash
   echo $DOCKER_HOST
   # Should show: unix:///Users/tim/.colima/default/docker.sock
   ```

3. Always use the `--container-daemon-socket ""` flag or the provided script

### Performance Tips

1. **Use `--reuse`** - Reuses containers between runs (enabled in `.actrc`)
2. **Parallel execution** - act runs matrix jobs in parallel by default
3. **Selective testing** - Use `-j <job-name>` to run specific jobs

## Comparison with GitHub Actions

| Feature | GitHub Actions | act with Colima |
|---------|---------------|-----------------|
| macOS runners | ✅ Native | ❌ Uses Linux containers |
| Secrets | ✅ Repository/Org secrets | ✅ Local `.secrets` file |
| Artifacts | ✅ Full support | ⚠️ Limited (local only) |
| Services | ✅ Docker services | ✅ Full support |
| Speed | Variable (queue time) | Fast (local execution) |
| Cost | Limited free minutes | Free (local resources) |

## Alternative: Direct Testing

If act doesn't work for your use case, you can run the validation script directly:

```bash
# Run all workflow validations without Docker
./validate-workflows.sh
```

This script simulates the key checks from the workflows:
- Ruff linting and formatting
- MyPy type checking
- Pytest test suite
- Package building
- Version consistency

## Summary

Using act with Colima requires disabling Docker socket mounting. The provided `act-colima.sh` script handles this configuration automatically, making it easy to test GitHub Actions workflows locally on macOS with Colima as the Docker runtime.