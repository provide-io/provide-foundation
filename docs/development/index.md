# Development

Contributing to provide.foundation.

- [Contributing](contributing.md) - How to contribute
- [CI/CD](ci-cd.md) - Build pipeline

## Architecture

See the [Architecture section](../architecture/index.md) for system design details.

## Testing

Run tests using pytest:
```bash
pytest                    # Run all tests
pytest -n auto           # Run tests in parallel
pytest tests/specific/   # Run specific tests
```

See the project's `pyproject.toml` for full test configuration.
