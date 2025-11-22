#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Polyglot Dependency Injection Pattern - Python Example.

This example demonstrates the dependency injection pattern that is
idiomatically identical across Python, Go, and Rust. This creates a
"golden cage" where the mental model is consistent across languages.

Compare this file with:
- 01_polyglot_di_pattern.go (Go version)
- 01_polyglot_di_pattern.rs (Rust version)

The structure is identical:
1. Define services with explicit constructor dependencies
2. Create Composition Root (main function)
3. Instantiate dependencies
4. Wire them together
5. Run application"""

from __future__ import annotations

from provide.foundation.hub import Container, injectable

# ==============================================================================
# Domain Models (Pure Business Logic - No Framework Dependencies)
# ==============================================================================


class User:
    """A user in our system."""

    def __init__(self, id: int, name: str, email: str) -> None:
        self.id = id
        self.name = name
        self.email = email


# ==============================================================================
# Infrastructure Layer (Implements Technical Concerns)
# ==============================================================================


class Database:
    """Database client for persistence."""

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        print(f"[Database] Connected to {connection_string}")

    def query(self, sql: str) -> list[dict[str, object]]:
        """Execute a SQL query."""
        print(f"[Database] Executing: {sql}")
        # Mock implementation
        return [{"id": 1, "name": "Alice", "email": "alice@example.com"}]


class HTTPClient:
    """HTTP client for external API calls."""

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        self.base_url = base_url
        self.timeout = timeout
        print(f"[HTTPClient] Configured for {base_url} (timeout: {timeout}s)")

    def post(self, path: str, data: dict[str, object]) -> dict[str, object]:
        """Send POST request."""
        url = f"{self.base_url}{path}"
        print(f"[HTTPClient] POST {url} with {data}")
        # Mock implementation
        return {"status": "success", "message": "User created"}


class Logger:
    """Application logger."""

    def __init__(self, level: str = "INFO") -> None:
        self.level = level
        print(f"[Logger] Initialized with level {level}")

    def info(self, message: str) -> None:
        """Log info message."""
        print(f"[INFO] {message}")

    def error(self, message: str) -> None:
        """Log error message."""
        print(f"[ERROR] {message}")


# ==============================================================================
# Application Layer (Business Logic Using Infrastructure)
# ==============================================================================


@injectable
class UserRepository:
    """Repository for user data access."""

    def __init__(self, db: Database, logger: Logger) -> None:
        """Initialize repository with dependencies.

        Note: Dependencies are explicit in the constructor signature.
        This is the same pattern as Go and Rust.
        """
        self.db = db
        self.logger = logger
        self.logger.info("UserRepository initialized")

    def find_by_id(self, user_id: int) -> User | None:
        """Find user by ID."""
        self.logger.info(f"Finding user {user_id}")
        rows = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
        if not rows:
            return None
        row = rows[0]
        return User(
            id=int(row["id"]),
            name=str(row["name"]),
            email=str(row["email"]),
        )


@injectable
class NotificationService:
    """Service for sending notifications."""

    def __init__(self, http_client: HTTPClient, logger: Logger) -> None:
        """Initialize service with dependencies."""
        self.http_client = http_client
        self.logger = logger
        self.logger.info("NotificationService initialized")

    def notify_user_created(self, user: User) -> bool:
        """Send notification when user is created."""
        self.logger.info(f"Sending notification for user {user.name}")
        response = self.http_client.post(
            "/notifications",
            {"user_id": user.id, "event": "user.created"},
        )
        return response.get("status") == "success"


@injectable
class UserService:
    """Core business logic for user operations."""

    def __init__(
        self,
        repository: UserRepository,
        notifications: NotificationService,
        logger: Logger,
    ) -> None:
        """Initialize service with dependencies.

        Note: This class depends on other application services.
        The container will resolve the entire dependency tree.
        """
        self.repository = repository
        self.notifications = notifications
        self.logger = logger
        self.logger.info("UserService initialized")

    def get_user(self, user_id: int) -> User | None:
        """Get a user and log the operation."""
        self.logger.info(f"Getting user {user_id}")
        user = self.repository.find_by_id(user_id)
        if user:
            self.logger.info(f"Found user: {user.name}")
            # Notify that user was accessed
            self.notifications.notify_user_created(user)
        return user


# ==============================================================================
# Composition Root (Application Entry Point)
# ==============================================================================


def main() -> None:
    """Application entry point - The Composition Root.

    This is where ALL dependency wiring happens. The pattern:
    1. Create DI Container
    2. Create and configure all dependencies
    3. Register dependencies by type
    4. Resolve application entry points
    5. Run the application

    This structure is IDENTICAL in Go and Rust.
    """
    print("=" * 70)
    print("Python Dependency Injection Example")
    print("=" * 70)

    # Step 1: Create the DI Container
    container = Container()

    # Step 2 & 3: Create and register infrastructure dependencies
    print("\n[Composition Root] Registering infrastructure dependencies...")
    container.register(Database, Database("postgresql://localhost/myapp"))
    container.register(HTTPClient, HTTPClient("https://api.example.com", timeout=30))
    container.register(Logger, Logger("INFO"))

    # Step 3: Register application services
    # Note: We don't instantiate these manually - the container will do it
    print("\n[Composition Root] Registering application services...")
    container.register(UserRepository, container.resolve(UserRepository))
    container.register(NotificationService, container.resolve(NotificationService))

    # Step 4: Resolve the main application service
    # The container automatically injects all dependencies
    print("\n[Composition Root] Resolving UserService...")
    user_service = container.resolve(UserService)

    # Step 5: Run the application
    print("\n" + "=" * 70)
    print("Running Application")
    print("=" * 70 + "\n")

    user = user_service.get_user(1)
    if user:
        print(f"\n✅ Retrieved user: {user.name} ({user.email})")
    else:
        print("\n❌ User not found")


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
