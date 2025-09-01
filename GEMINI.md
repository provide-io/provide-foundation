# GEMINI.md: Your AI Assistant for the `provide-foundation` Project

This document provides context and instructions for interacting with the `provide-foundation` project. It is intended to be used by the Gemini AI assistant to help you with your development tasks.

## Project Overview

`provide.foundation` is a Python library that provides a beautiful, performant, and structured logging experience. It is built on top of the popular `structlog` library and adds a number of features, including:

*   **Emoji-enhanced visual parsing:** Emoji prefixes based on logger names and semantic context make logs instantly scannable.
*   **Semantic logging:** Extensible Semantic Layers for domains like LLMs, HTTP, and Databases, with a fallback to the classic Domain-Action-Status (DAS) pattern.
*   **High performance:** Benchmarked at over 14,000 messages per second.
*   **Zero configuration:** Works out of the box, but can be configured via environment variables or code.
*   **Developer-friendly:** Thread-safe, async-ready, and comes with comprehensive type hints.

## Building and Running

The project is built and managed using standard Python tooling. Here are the key commands:

*   **Install dependencies:**
    ```bash
    pip install -e .
    ```
*   **Run tests:**
    ```bash
    pytest
    ```
*   **Run linting and formatting:**
    ```bash
    ruff check .
    ruff format .
    ```
*   **Run type checking:**
    ```bash
    mypy src
    ```

## Development Conventions

The project follows standard Python development conventions. Here are some of the key ones:

*   **Code style:** The code is formatted with `ruff format` and linted with `ruff check`.
*   **Testing:** The project is tested with `pytest`.
*   **Type checking:** Type checking is done with `mypy`.
*   **Dependencies:** Dependencies are managed with `pip` and specified in the `pyproject.toml` file.
