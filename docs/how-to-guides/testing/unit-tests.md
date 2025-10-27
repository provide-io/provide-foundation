# Unit Testing

Learn how to write unit tests for Foundation applications.

## Overview

Foundation provides testing utilities through the `provide-testkit` package.

## Basic Test Setup

```python
import pytest
from provide.testkit import reset_foundation_setup_for_testing

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation before each test."""
    reset_foundation_setup_for_testing()

def test_logging():
    """Test logging works correctly."""
    from provide.foundation import logger

    logger.info("test_event", value=123)
    # Assert log was created
```

## Testing with FoundationTestCase

```python
from provide.testkit import FoundationTestCase

class TestMyFeature(FoundationTestCase):
    def setup_method(self):
        """Set up test environment."""
        super().setup_method()
        self.data = {"key": "value"}

    def test_feature(self):
        """Test a feature."""
        assert self.data["key"] == "value"

    def teardown_method(self):
        """Clean up after test."""
        super().teardown_method()
```

## Capturing Logs

```python
from provide.testkit import set_log_stream_for_testing
from io import StringIO

def test_log_output():
    """Test log output content."""
    stream = StringIO()
    set_log_stream_for_testing(stream)

    from provide.foundation import logger
    logger.info("test_message", value=42)

    output = stream.getvalue()
    assert "test_message" in output
    assert "value=42" in output
```

## Next Steps

- **[Testing CLI Commands](cli-tests.md)** - Test CLI apps
- **[API Reference](../../reference/provide/foundation/index.md)**

**See also:** [CLAUDE.md - Testing Strategy](../../CLAUDE.md#testing-strategy)
