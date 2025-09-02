# 📚 API Reference

## Configuration

This section provides a detailed reference for the data classes and functions used to configure the `provide.foundation` telemetry system.

---

### Core Setup Function

This is the main function for applying configuration. It should be called once at application startup.

::: provide.foundation.core.setup_telemetry

---

### `TelemetryConfig`

This is the top-level data class for all telemetry configuration.

::: provide.foundation.logger.config.TelemetryConfig
    options:
      show_root_heading: false
      members:
        - service_name
        - logging
        - globally_disabled
        - from_env

---

### `LoggingConfig`

This data class holds all configuration options related to the logging system.

::: provide.foundation.logger.config.LoggingConfig
    options:
      show_root_heading: false