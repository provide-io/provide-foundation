#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for the error handling system."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors import (
    AlreadyExistsError,
    NetworkError,
    ValidationError,
    transactional,
)
from provide.foundation.resilience import circuit_breaker, retry


class TestRealWorldScenarios(FoundationTestCase):
    """Test real-world error handling scenarios."""

    def test_web_request_error_handling(self) -> None:
        """Simulate web request error handling."""
        # Simulate request context
        request_data = {
            "method": "POST",
            "path": "/api/users",
            "headers": {"X-Request-ID": "req_abc123"},
            "body": {"email": "invalid", "age": -1},
        }

        def validate_request(data: dict[str, dict[str, str]]) -> None:
            errors = []

            if "@" not in data.get("body", {}).get("email", ""):
                errors.append(ValidationError("Invalid email", field="email"))

            if data.get("body", {}).get("age", 0) < 0:
                errors.append(ValidationError("Age must be positive", field="age"))

            if errors:
                raise ValidationError(
                    "Request validation failed",
                    validation_errors=[str(e) for e in errors],
                    request_id=data["headers"]["X-Request-ID"],
                )

        # Handle request
        try:
            validate_request(request_data)
        except ValidationError as e:
            # Create error response
            assert e.context["request_id"] == "req_abc123"
            assert len(e.context["validation_errors"]) == 2

    def test_database_transaction_error(self) -> None:
        """Simulate database transaction error handling."""
        db_operations = []

        def db_insert(table: str, data: dict[str, str]) -> None:
            db_operations.append(("insert", table, data))
            if table == "users" and data.get("email") == "duplicate@example.com":
                raise AlreadyExistsError(
                    "User already exists",
                    resource_type="user",
                    resource_id=data["email"],
                )

        def db_rollback() -> None:
            db_operations.append(("rollback", None, None))

        def db_commit() -> None:
            db_operations.append(("commit", None, None))

        # Successful transaction
        with transactional(db_rollback, db_commit):
            db_insert("users", {"email": "new@example.com"})
            db_insert("profiles", {"user_email": "new@example.com"})

        assert ("commit", None, None) in db_operations

        # Failed transaction
        db_operations.clear()

        with pytest.raises(AlreadyExistsError), transactional(db_rollback, db_commit):
            db_insert("users", {"email": "duplicate@example.com"})
            db_insert("profiles", {"user_email": "duplicate@example.com"})

        assert ("rollback", None, None) in db_operations
        assert ("commit", None, None) not in db_operations

    def test_microservice_communication_error(self) -> None:
        """Simulate microservice communication error handling."""
        service_calls = []

        @retry(NetworkError, max_attempts=3, base_delay=0.01)
        @circuit_breaker(failure_threshold=5, recovery_timeout=0.1)
        def call_user_service(user_id: int) -> dict[str, str | int]:
            service_calls.append(("user-service", user_id))

            # Simulate intermittent failures
            if len(service_calls) < 2:
                raise NetworkError(
                    "Connection timeout",
                    service="user-service",
                    endpoint=f"/users/{user_id}",
                )

            return {"id": user_id, "name": "Test User"}

        # Should retry and succeed
        result = call_user_service(123)
        assert result["id"] == 123
        assert len(service_calls) == 2  # One failure, one success


# 🧱🏗️🔚
