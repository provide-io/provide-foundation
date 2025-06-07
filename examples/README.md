# Pyvider Telemetry Examples

This directory contains a collection of executable Python scripts demonstrating various features and usage patterns of the `pyvider-telemetry` library. Each script is designed to be run independently and showcases a specific aspect of the library.

## Running the Examples

To run an example script:

1.  **Navigate to this directory** in your terminal:
    ```bash
    cd examples/pyvider_telemetry
    ```

2.  **Execute the desired Python script**:
    ```bash
    python <example_file_name>.py
    ```
    For example, to run the quick start example:
    ```bash
    python 01_quick_start.py
    ```

Each script will print output to the console, typically including formatted log messages that demonstrate the feature being showcased. The `sys.path` is manipulated at the beginning of each script to ensure it can find the `pyvider.telemetry` module from the project's `src` directory.

## Example Files

Here's a list of the available examples and what they demonstrate:

-   **`01_quick_start.py`**:
    Shows the most basic setup and logging calls using the default configuration of Pyvider Telemetry.

-   **`02_custom_configuration.py`**:
    Illustrates how to programmatically configure Pyvider Telemetry using `TelemetryConfig` and `LoggingConfig` objects to control aspects like service name, log levels, and output formats (e.g., JSON).

-   **`03_named_loggers.py`**:
    Demonstrates creating and using component-specific named loggers obtained via `logger.get_logger()`, which helps in identifying log sources and enabling fine-grained filtering.

-   **`04_das_logging.py`**:
    Showcases Domain-Action-Status (DAS) structured logging. This pattern uses `domain`, `action`, and `status` keys in log events for semantic meaning, often enhanced with emojis.

-   **`05_exception_handling.py`**:
    Illustrates how to properly log Python exceptions, ensuring that tracebacks are automatically included in the log output using `logger.exception()`.

-   **`06_trace_logging.py`**:
    Demonstrates the usage of the custom `TRACE` log level, which is intended for ultra-verbose diagnostic output, and how to enable it.

-   **`07_module_filtering.py`**:
    Shows how to configure module-specific log levels, allowing different parts of an application to have different log verbosities (e.g., more verbose for a specific module, less for others).

-   **`08_env_variables_config.py`**:
    Illustrates how Pyvider Telemetry can be configured entirely through environment variables (e.g., `PYVIDER_LOG_LEVEL`, `PYVIDER_SERVICE_NAME`), allowing for runtime adjustments without code changes.

-   **`09_async_usage.py`**:
    Provides examples of using Pyvider Telemetry in asynchronous applications built with `asyncio`, including logging from async functions and using `shutdown_pyvider_telemetry()`.

-   **`10_production_patterns.py`**:
    Demonstrates logging patterns and configurations suitable for production environments, such as structured JSON logging, appropriate log levels, and logging key business events or health metrics.

## Exploration

Feel free to explore, modify, and run these examples to better understand the capabilities and configuration options of the `pyvider-telemetry` library. Each script is self-contained and can be a good starting point for integrating Pyvider Telemetry into your own projects.
