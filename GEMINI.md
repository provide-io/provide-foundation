# GEMINI.md: Your AI Assistant for the `provide-foundation` Project

This document provides context and instructions for interacting with the `provide-foundation` project. It is intended to be used by the Gemini AI assistant to help you with your development tasks.

## Project Overview

`provide-foundation` is a comprehensive foundation library for Python applications, offering structured logging, CLI utilities, configuration management, error handling, and essential application building blocks. Built with modern Python practices, it provides the core infrastructure that production applications need.

The project uses `uv` for package management and `pytest` for testing. The code is linted with `ruff` and type-checked with `mypy`.

## Building and Running

The project can be built and tested using the commands in the `Makefile`.

*   **Setup**: `make setup` - Creates a virtual environment and installs dependencies.
*   **Test**: `make test` - Runs the full test suite.
*   **Lint**: `make lint` - Runs `ruff` to format and lint the code.
*   **Type Check**: `make typecheck` - Runs `mypy` to perform static type checking.
*   **Coverage**: `make coverage` - Runs tests with a coverage report.
*   **Build**: `make build` - Builds the package.
*   **All**: `make all` - Runs lint, typecheck, and tests.

The CLI entry point is `foundation`, which can be run with `python -m provide.foundation.cli.main`.

## Development Conventions

*   **Coding Style**: The code is formatted with `ruff format` and linted with `ruff check`.
*   **Testing**: The project is tested with `pytest`. Tests are located in the `tests` directory.
*   **Type Checking**: Type checking is done with `mypy`.
*   **Dependencies**: Dependencies are managed with `uv` and specified in the `pyproject.toml` file.
*   **Virtual Environments**: The project is developed in a virtual environment, which can be managed with the `make setup` command.
