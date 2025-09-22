# Makefile for provide-foundation development

.PHONY: help setup test lint typecheck coverage clean build all

# Default target
help:
	@echo "Available targets:"
	@echo "  setup     - Create virtual environment and install dependencies"
	@echo "  test      - Run full test suite"
	@echo "  lint      - Run ruff format and check with fixes"
	@echo "  typecheck - Run mypy type checking"
	@echo "  coverage  - Run tests with coverage report"
	@echo "  clean     - Remove virtual environment and cache files"
	@echo "  build     - Build the package"
	@echo "  all       - Run lint, typecheck, and tests"

# Create virtual environment and install dependencies
setup:
	@echo "Creating virtual environment..."
	uv venv
	@echo "Installing dependencies..."
	uv sync
	@echo "Setup complete! Activate with: source .venv/bin/activate"

# Run full test suite
test:
	@echo "Running test suite..."
	source .venv/bin/activate && python -m pytest

# Run ruff format and check with fixes
lint:
	@echo "Running ruff format..."
	source .venv/bin/activate && ruff format src/ tests/
	@echo "Running ruff check with fixes..."
	source .venv/bin/activate && ruff check src/ tests/ --fix --unsafe-fixes

# Run mypy type checking
typecheck:
	@echo "Running mypy type checking..."
	source .venv/bin/activate && mypy src/

# Run tests with coverage report
coverage:
	@echo "Running tests with coverage..."
	source .venv/bin/activate && python -m pytest --cov=src --cov-report=html --cov-report=term

# Remove virtual environment and cache files
clean:
	@echo "Cleaning up..."
	rm -rf .venv/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Build the package
build:
	@echo "Building package..."
	source .venv/bin/activate && uv build

# Run all quality checks
all: lint typecheck test
	@echo "All checks completed!"