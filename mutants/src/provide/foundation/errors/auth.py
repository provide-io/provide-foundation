# provide/foundation/errors/auth.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Authentication and authorization exceptions."""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class AuthenticationError(FoundationError):
    """Raised when authentication fails.

    Args:
        message: Error message describing the authentication failure.
        auth_method: Optional authentication method used.
        realm: Optional authentication realm.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise AuthenticationError("Invalid credentials")
        >>> raise AuthenticationError("Token expired", auth_method="jwt")

    """

    def xǁAuthenticationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = None
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault(None, {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", None)["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault({})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault(
                "context",
            )["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("XXcontextXX", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("CONTEXT", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["XXauth.methodXX"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["AUTH.METHOD"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = None
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault(None, {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", None)["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault({})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault(
                "context",
            )["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("XXcontextXX", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("CONTEXT", {})["auth.realm"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["XXauth.realmXX"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["AUTH.REALM"] = realm
        super().__init__(message, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(None, **kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(**kwargs)

    def xǁAuthenticationErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        auth_method: str | None = None,
        realm: str | None = None,
        **kwargs: Any,
    ) -> None:
        if auth_method:
            kwargs.setdefault("context", {})["auth.method"] = auth_method
        if realm:
            kwargs.setdefault("context", {})["auth.realm"] = realm
        super().__init__(
            message,
        )

    xǁAuthenticationErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAuthenticationErrorǁ__init____mutmut_1": xǁAuthenticationErrorǁ__init____mutmut_1,
        "xǁAuthenticationErrorǁ__init____mutmut_2": xǁAuthenticationErrorǁ__init____mutmut_2,
        "xǁAuthenticationErrorǁ__init____mutmut_3": xǁAuthenticationErrorǁ__init____mutmut_3,
        "xǁAuthenticationErrorǁ__init____mutmut_4": xǁAuthenticationErrorǁ__init____mutmut_4,
        "xǁAuthenticationErrorǁ__init____mutmut_5": xǁAuthenticationErrorǁ__init____mutmut_5,
        "xǁAuthenticationErrorǁ__init____mutmut_6": xǁAuthenticationErrorǁ__init____mutmut_6,
        "xǁAuthenticationErrorǁ__init____mutmut_7": xǁAuthenticationErrorǁ__init____mutmut_7,
        "xǁAuthenticationErrorǁ__init____mutmut_8": xǁAuthenticationErrorǁ__init____mutmut_8,
        "xǁAuthenticationErrorǁ__init____mutmut_9": xǁAuthenticationErrorǁ__init____mutmut_9,
        "xǁAuthenticationErrorǁ__init____mutmut_10": xǁAuthenticationErrorǁ__init____mutmut_10,
        "xǁAuthenticationErrorǁ__init____mutmut_11": xǁAuthenticationErrorǁ__init____mutmut_11,
        "xǁAuthenticationErrorǁ__init____mutmut_12": xǁAuthenticationErrorǁ__init____mutmut_12,
        "xǁAuthenticationErrorǁ__init____mutmut_13": xǁAuthenticationErrorǁ__init____mutmut_13,
        "xǁAuthenticationErrorǁ__init____mutmut_14": xǁAuthenticationErrorǁ__init____mutmut_14,
        "xǁAuthenticationErrorǁ__init____mutmut_15": xǁAuthenticationErrorǁ__init____mutmut_15,
        "xǁAuthenticationErrorǁ__init____mutmut_16": xǁAuthenticationErrorǁ__init____mutmut_16,
        "xǁAuthenticationErrorǁ__init____mutmut_17": xǁAuthenticationErrorǁ__init____mutmut_17,
        "xǁAuthenticationErrorǁ__init____mutmut_18": xǁAuthenticationErrorǁ__init____mutmut_18,
        "xǁAuthenticationErrorǁ__init____mutmut_19": xǁAuthenticationErrorǁ__init____mutmut_19,
        "xǁAuthenticationErrorǁ__init____mutmut_20": xǁAuthenticationErrorǁ__init____mutmut_20,
        "xǁAuthenticationErrorǁ__init____mutmut_21": xǁAuthenticationErrorǁ__init____mutmut_21,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAuthenticationErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁAuthenticationErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁAuthenticationErrorǁ__init____mutmut_orig)
    xǁAuthenticationErrorǁ__init____mutmut_orig.__name__ = "xǁAuthenticationErrorǁ__init__"

    def xǁAuthenticationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "AUTH_ERROR"

    def xǁAuthenticationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXAUTH_ERRORXX"

    def xǁAuthenticationErrorǁ_default_code__mutmut_2(self) -> str:
        return "auth_error"

    xǁAuthenticationErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAuthenticationErrorǁ_default_code__mutmut_1": xǁAuthenticationErrorǁ_default_code__mutmut_1,
        "xǁAuthenticationErrorǁ_default_code__mutmut_2": xǁAuthenticationErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAuthenticationErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁAuthenticationErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁAuthenticationErrorǁ_default_code__mutmut_orig)
    xǁAuthenticationErrorǁ_default_code__mutmut_orig.__name__ = "xǁAuthenticationErrorǁ_default_code"


class AuthorizationError(FoundationError):
    """Raised when authorization fails.

    Args:
        message: Error message describing the authorization failure.
        required_permission: Optional required permission.
        resource: Optional resource being accessed.
        actor: Optional actor (user/service) attempting access.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise AuthorizationError("Access denied")
        >>> raise AuthorizationError("Insufficient permissions", required_permission="admin")

    """

    def xǁAuthorizationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = None
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault(None, {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", None)["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault({})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault(
                "context",
            )["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("XXcontextXX", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("CONTEXT", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["XXauthz.permissionXX"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["AUTHZ.PERMISSION"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = None
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault(None, {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", None)["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault({})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault(
                "context",
            )["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("XXcontextXX", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("CONTEXT", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["XXauthz.resourceXX"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["AUTHZ.RESOURCE"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = None
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault(None, {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", None)["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault({})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault(
                "context",
            )["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("XXcontextXX", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("CONTEXT", {})["authz.actor"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["XXauthz.actorXX"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_27(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["AUTHZ.ACTOR"] = actor
        super().__init__(message, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_28(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(None, **kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_29(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(**kwargs)

    def xǁAuthorizationErrorǁ__init____mutmut_30(
        self,
        message: str,
        *,
        required_permission: str | None = None,
        resource: str | None = None,
        actor: str | None = None,
        **kwargs: Any,
    ) -> None:
        if required_permission:
            kwargs.setdefault("context", {})["authz.permission"] = required_permission
        if resource:
            kwargs.setdefault("context", {})["authz.resource"] = resource
        if actor:
            kwargs.setdefault("context", {})["authz.actor"] = actor
        super().__init__(
            message,
        )

    xǁAuthorizationErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAuthorizationErrorǁ__init____mutmut_1": xǁAuthorizationErrorǁ__init____mutmut_1,
        "xǁAuthorizationErrorǁ__init____mutmut_2": xǁAuthorizationErrorǁ__init____mutmut_2,
        "xǁAuthorizationErrorǁ__init____mutmut_3": xǁAuthorizationErrorǁ__init____mutmut_3,
        "xǁAuthorizationErrorǁ__init____mutmut_4": xǁAuthorizationErrorǁ__init____mutmut_4,
        "xǁAuthorizationErrorǁ__init____mutmut_5": xǁAuthorizationErrorǁ__init____mutmut_5,
        "xǁAuthorizationErrorǁ__init____mutmut_6": xǁAuthorizationErrorǁ__init____mutmut_6,
        "xǁAuthorizationErrorǁ__init____mutmut_7": xǁAuthorizationErrorǁ__init____mutmut_7,
        "xǁAuthorizationErrorǁ__init____mutmut_8": xǁAuthorizationErrorǁ__init____mutmut_8,
        "xǁAuthorizationErrorǁ__init____mutmut_9": xǁAuthorizationErrorǁ__init____mutmut_9,
        "xǁAuthorizationErrorǁ__init____mutmut_10": xǁAuthorizationErrorǁ__init____mutmut_10,
        "xǁAuthorizationErrorǁ__init____mutmut_11": xǁAuthorizationErrorǁ__init____mutmut_11,
        "xǁAuthorizationErrorǁ__init____mutmut_12": xǁAuthorizationErrorǁ__init____mutmut_12,
        "xǁAuthorizationErrorǁ__init____mutmut_13": xǁAuthorizationErrorǁ__init____mutmut_13,
        "xǁAuthorizationErrorǁ__init____mutmut_14": xǁAuthorizationErrorǁ__init____mutmut_14,
        "xǁAuthorizationErrorǁ__init____mutmut_15": xǁAuthorizationErrorǁ__init____mutmut_15,
        "xǁAuthorizationErrorǁ__init____mutmut_16": xǁAuthorizationErrorǁ__init____mutmut_16,
        "xǁAuthorizationErrorǁ__init____mutmut_17": xǁAuthorizationErrorǁ__init____mutmut_17,
        "xǁAuthorizationErrorǁ__init____mutmut_18": xǁAuthorizationErrorǁ__init____mutmut_18,
        "xǁAuthorizationErrorǁ__init____mutmut_19": xǁAuthorizationErrorǁ__init____mutmut_19,
        "xǁAuthorizationErrorǁ__init____mutmut_20": xǁAuthorizationErrorǁ__init____mutmut_20,
        "xǁAuthorizationErrorǁ__init____mutmut_21": xǁAuthorizationErrorǁ__init____mutmut_21,
        "xǁAuthorizationErrorǁ__init____mutmut_22": xǁAuthorizationErrorǁ__init____mutmut_22,
        "xǁAuthorizationErrorǁ__init____mutmut_23": xǁAuthorizationErrorǁ__init____mutmut_23,
        "xǁAuthorizationErrorǁ__init____mutmut_24": xǁAuthorizationErrorǁ__init____mutmut_24,
        "xǁAuthorizationErrorǁ__init____mutmut_25": xǁAuthorizationErrorǁ__init____mutmut_25,
        "xǁAuthorizationErrorǁ__init____mutmut_26": xǁAuthorizationErrorǁ__init____mutmut_26,
        "xǁAuthorizationErrorǁ__init____mutmut_27": xǁAuthorizationErrorǁ__init____mutmut_27,
        "xǁAuthorizationErrorǁ__init____mutmut_28": xǁAuthorizationErrorǁ__init____mutmut_28,
        "xǁAuthorizationErrorǁ__init____mutmut_29": xǁAuthorizationErrorǁ__init____mutmut_29,
        "xǁAuthorizationErrorǁ__init____mutmut_30": xǁAuthorizationErrorǁ__init____mutmut_30,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAuthorizationErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁAuthorizationErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁAuthorizationErrorǁ__init____mutmut_orig)
    xǁAuthorizationErrorǁ__init____mutmut_orig.__name__ = "xǁAuthorizationErrorǁ__init__"

    def xǁAuthorizationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "AUTHZ_ERROR"

    def xǁAuthorizationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXAUTHZ_ERRORXX"

    def xǁAuthorizationErrorǁ_default_code__mutmut_2(self) -> str:
        return "authz_error"

    xǁAuthorizationErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁAuthorizationErrorǁ_default_code__mutmut_1": xǁAuthorizationErrorǁ_default_code__mutmut_1,
        "xǁAuthorizationErrorǁ_default_code__mutmut_2": xǁAuthorizationErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁAuthorizationErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁAuthorizationErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁAuthorizationErrorǁ_default_code__mutmut_orig)
    xǁAuthorizationErrorǁ_default_code__mutmut_orig.__name__ = "xǁAuthorizationErrorǁ_default_code"


# <3 🧱🤝🐛🪄
