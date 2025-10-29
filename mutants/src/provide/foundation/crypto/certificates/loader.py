# provide/foundation/crypto/certificates/loader.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from datetime import UTC
import os
from pathlib import Path
import traceback
from typing import TYPE_CHECKING

from provide.foundation import logger
from provide.foundation.crypto.certificates.base import (
    CertificateBase,
    CertificateError,
)

"""Certificate loading utilities."""

if TYPE_CHECKING:
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

try:
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False
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


def x_load_from_uri_or_pem__mutmut_orig(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_1(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith(None):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_2(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("XXfile://XX"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_3(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("FILE://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_4(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = None
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_5(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix(None)
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_6(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removesuffix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_7(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("XXfile://XX")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_8(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("FILE://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_9(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" or path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_10(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name != "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_11(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "XXntXX" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_12(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "NT" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_13(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith(None):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_14(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("XX//XX"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_15(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = None
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_16(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(None)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_17(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = None
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_18(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip(None)
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_19(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.rstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_20(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("XX/XX")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_21(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" or data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_22(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name == "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_23(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "XXntXX" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_24(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "NT" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_25(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith(None):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_26(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("XXfile:///XX"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_27(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("FILE:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_28(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = None
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_29(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" - path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_30(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "XX/XX" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_31(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = None

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_32(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(None)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_33(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(None)
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_34(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open(None, encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_35(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding=None) as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_36(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open(encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_37(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open(
                "r",
            ) as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_38(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("XXrXX", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_39(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("R", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_40(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="XXutf-8XX") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_41(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="UTF-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_42(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = None
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_43(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug(None)
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_44(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("XX📜📂✅ Loaded data from fileXX")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_45(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_46(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ LOADED DATA FROM FILE")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_47(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = None
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_48(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_49(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith(None):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_50(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("XX-----BEGINXX"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_51(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----begin"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_52(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning(None)
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_53(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("XX📜📂⚠️ Data doesn't look like PEM formatXX")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_54(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ data doesn't look like pem format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_55(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ DATA DOESN'T LOOK LIKE PEM FORMAT")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_56(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(None, extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_57(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra=None)
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_58(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(extra={"error": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_59(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(
            f"📜📂❌ Failed to load data: {e}",
        )
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_60(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"XXerrorXX": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_61(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"ERROR": str(e)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_62(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(None)})
        raise CertificateError(f"Failed to load data: {e}") from e


def x_load_from_uri_or_pem__mutmut_63(data: str) -> str:
    """Load PEM data either directly from a string or from a file URI."""
    try:
        if data.startswith("file://"):
            path_str = data.removeprefix("file://")
            if os.name == "nt" and path_str.startswith("//"):
                path = Path(path_str)
            else:
                path_str = path_str.lstrip("/")
                if os.name != "nt" and data.startswith("file:///"):
                    path_str = "/" + path_str
                path = Path(path_str)

            logger.debug(f"📜📂🚀 Loading data from file: {path}")
            with path.open("r", encoding="utf-8") as f:
                loaded_data = f.read().strip()
            logger.debug("📜📂✅ Loaded data from file")
            return loaded_data

        loaded_data = data.strip()
        if not loaded_data.startswith("-----BEGIN"):
            logger.warning("📜📂⚠️ Data doesn't look like PEM format")
        return loaded_data
    except Exception as e:
        logger.error(f"📜📂❌ Failed to load data: {e}", extra={"error": str(e)})
        raise CertificateError(None) from e


x_load_from_uri_or_pem__mutmut_mutants: ClassVar[MutantDict] = {
    "x_load_from_uri_or_pem__mutmut_1": x_load_from_uri_or_pem__mutmut_1,
    "x_load_from_uri_or_pem__mutmut_2": x_load_from_uri_or_pem__mutmut_2,
    "x_load_from_uri_or_pem__mutmut_3": x_load_from_uri_or_pem__mutmut_3,
    "x_load_from_uri_or_pem__mutmut_4": x_load_from_uri_or_pem__mutmut_4,
    "x_load_from_uri_or_pem__mutmut_5": x_load_from_uri_or_pem__mutmut_5,
    "x_load_from_uri_or_pem__mutmut_6": x_load_from_uri_or_pem__mutmut_6,
    "x_load_from_uri_or_pem__mutmut_7": x_load_from_uri_or_pem__mutmut_7,
    "x_load_from_uri_or_pem__mutmut_8": x_load_from_uri_or_pem__mutmut_8,
    "x_load_from_uri_or_pem__mutmut_9": x_load_from_uri_or_pem__mutmut_9,
    "x_load_from_uri_or_pem__mutmut_10": x_load_from_uri_or_pem__mutmut_10,
    "x_load_from_uri_or_pem__mutmut_11": x_load_from_uri_or_pem__mutmut_11,
    "x_load_from_uri_or_pem__mutmut_12": x_load_from_uri_or_pem__mutmut_12,
    "x_load_from_uri_or_pem__mutmut_13": x_load_from_uri_or_pem__mutmut_13,
    "x_load_from_uri_or_pem__mutmut_14": x_load_from_uri_or_pem__mutmut_14,
    "x_load_from_uri_or_pem__mutmut_15": x_load_from_uri_or_pem__mutmut_15,
    "x_load_from_uri_or_pem__mutmut_16": x_load_from_uri_or_pem__mutmut_16,
    "x_load_from_uri_or_pem__mutmut_17": x_load_from_uri_or_pem__mutmut_17,
    "x_load_from_uri_or_pem__mutmut_18": x_load_from_uri_or_pem__mutmut_18,
    "x_load_from_uri_or_pem__mutmut_19": x_load_from_uri_or_pem__mutmut_19,
    "x_load_from_uri_or_pem__mutmut_20": x_load_from_uri_or_pem__mutmut_20,
    "x_load_from_uri_or_pem__mutmut_21": x_load_from_uri_or_pem__mutmut_21,
    "x_load_from_uri_or_pem__mutmut_22": x_load_from_uri_or_pem__mutmut_22,
    "x_load_from_uri_or_pem__mutmut_23": x_load_from_uri_or_pem__mutmut_23,
    "x_load_from_uri_or_pem__mutmut_24": x_load_from_uri_or_pem__mutmut_24,
    "x_load_from_uri_or_pem__mutmut_25": x_load_from_uri_or_pem__mutmut_25,
    "x_load_from_uri_or_pem__mutmut_26": x_load_from_uri_or_pem__mutmut_26,
    "x_load_from_uri_or_pem__mutmut_27": x_load_from_uri_or_pem__mutmut_27,
    "x_load_from_uri_or_pem__mutmut_28": x_load_from_uri_or_pem__mutmut_28,
    "x_load_from_uri_or_pem__mutmut_29": x_load_from_uri_or_pem__mutmut_29,
    "x_load_from_uri_or_pem__mutmut_30": x_load_from_uri_or_pem__mutmut_30,
    "x_load_from_uri_or_pem__mutmut_31": x_load_from_uri_or_pem__mutmut_31,
    "x_load_from_uri_or_pem__mutmut_32": x_load_from_uri_or_pem__mutmut_32,
    "x_load_from_uri_or_pem__mutmut_33": x_load_from_uri_or_pem__mutmut_33,
    "x_load_from_uri_or_pem__mutmut_34": x_load_from_uri_or_pem__mutmut_34,
    "x_load_from_uri_or_pem__mutmut_35": x_load_from_uri_or_pem__mutmut_35,
    "x_load_from_uri_or_pem__mutmut_36": x_load_from_uri_or_pem__mutmut_36,
    "x_load_from_uri_or_pem__mutmut_37": x_load_from_uri_or_pem__mutmut_37,
    "x_load_from_uri_or_pem__mutmut_38": x_load_from_uri_or_pem__mutmut_38,
    "x_load_from_uri_or_pem__mutmut_39": x_load_from_uri_or_pem__mutmut_39,
    "x_load_from_uri_or_pem__mutmut_40": x_load_from_uri_or_pem__mutmut_40,
    "x_load_from_uri_or_pem__mutmut_41": x_load_from_uri_or_pem__mutmut_41,
    "x_load_from_uri_or_pem__mutmut_42": x_load_from_uri_or_pem__mutmut_42,
    "x_load_from_uri_or_pem__mutmut_43": x_load_from_uri_or_pem__mutmut_43,
    "x_load_from_uri_or_pem__mutmut_44": x_load_from_uri_or_pem__mutmut_44,
    "x_load_from_uri_or_pem__mutmut_45": x_load_from_uri_or_pem__mutmut_45,
    "x_load_from_uri_or_pem__mutmut_46": x_load_from_uri_or_pem__mutmut_46,
    "x_load_from_uri_or_pem__mutmut_47": x_load_from_uri_or_pem__mutmut_47,
    "x_load_from_uri_or_pem__mutmut_48": x_load_from_uri_or_pem__mutmut_48,
    "x_load_from_uri_or_pem__mutmut_49": x_load_from_uri_or_pem__mutmut_49,
    "x_load_from_uri_or_pem__mutmut_50": x_load_from_uri_or_pem__mutmut_50,
    "x_load_from_uri_or_pem__mutmut_51": x_load_from_uri_or_pem__mutmut_51,
    "x_load_from_uri_or_pem__mutmut_52": x_load_from_uri_or_pem__mutmut_52,
    "x_load_from_uri_or_pem__mutmut_53": x_load_from_uri_or_pem__mutmut_53,
    "x_load_from_uri_or_pem__mutmut_54": x_load_from_uri_or_pem__mutmut_54,
    "x_load_from_uri_or_pem__mutmut_55": x_load_from_uri_or_pem__mutmut_55,
    "x_load_from_uri_or_pem__mutmut_56": x_load_from_uri_or_pem__mutmut_56,
    "x_load_from_uri_or_pem__mutmut_57": x_load_from_uri_or_pem__mutmut_57,
    "x_load_from_uri_or_pem__mutmut_58": x_load_from_uri_or_pem__mutmut_58,
    "x_load_from_uri_or_pem__mutmut_59": x_load_from_uri_or_pem__mutmut_59,
    "x_load_from_uri_or_pem__mutmut_60": x_load_from_uri_or_pem__mutmut_60,
    "x_load_from_uri_or_pem__mutmut_61": x_load_from_uri_or_pem__mutmut_61,
    "x_load_from_uri_or_pem__mutmut_62": x_load_from_uri_or_pem__mutmut_62,
    "x_load_from_uri_or_pem__mutmut_63": x_load_from_uri_or_pem__mutmut_63,
}


def load_from_uri_or_pem(*args, **kwargs):
    result = _mutmut_trampoline(
        x_load_from_uri_or_pem__mutmut_orig, x_load_from_uri_or_pem__mutmut_mutants, args, kwargs
    )
    return result


load_from_uri_or_pem.__signature__ = _mutmut_signature(x_load_from_uri_or_pem__mutmut_orig)
x_load_from_uri_or_pem__mutmut_orig.__name__ = "x_load_from_uri_or_pem"


def x_load_certificate_from_pem__mutmut_orig(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_1(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug(None)
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_2(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("XX📜🔑🚀 Loading certificate from provided dataXX")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_3(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_4(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 LOADING CERTIFICATE FROM PROVIDED DATA")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_5(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = None

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_6(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(None)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_7(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug(None)
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_8(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("XX📜🔑🔍 Loading X.509 certificate from PEM dataXX")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_9(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 loading x.509 certificate from pem data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_10(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 LOADING X.509 CERTIFICATE FROM PEM DATA")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_11(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = None
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_12(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(None)
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_13(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode(None))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_14(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("XXutf-8XX"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_15(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("UTF-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_16(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug(None)

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_17(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("XX📜🔑✅ X.509 certificate object loaded from PEMXX")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_18(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ x.509 certificate object loaded from pem")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_19(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 CERTIFICATE OBJECT LOADED FROM PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_20(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = ""
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_21(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = ""

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_22(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug(None)
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_23(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("XX📜🔑🚀 Loading private keyXX")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_24(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_25(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 LOADING PRIVATE KEY")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_26(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = None

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_27(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(None)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_28(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = None
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_29(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(None, password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_30(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_31(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(
                key_data.encode("utf-8"),
            )
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_32(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode(None), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_33(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("XXutf-8XX"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_34(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("UTF-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_35(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_36(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    None,
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_37(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(None)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_38(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "XXExpected RSA or ECDSA private key.XX",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_39(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "expected rsa or ecdsa private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_40(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "EXPECTED RSA OR ECDSA PRIVATE KEY.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_41(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = None
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_42(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug(None)

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_43(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("XX📜🔑✅ Private key object loaded and type validatedXX")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_44(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_45(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ PRIVATE KEY OBJECT LOADED AND TYPE VALIDATED")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_46(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = None  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_47(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = None  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_48(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is not None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_49(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = None
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_50(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=None)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_51(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is not None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_52(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = None

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_53(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=None)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_54(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = None
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_55(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_56(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                None,
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_57(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(None)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_58(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "XXExpected RSA or ECDSA public key.XX",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_59(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "expected rsa or ecdsa public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_60(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "EXPECTED RSA OR ECDSA PUBLIC KEY.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_61(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = None
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_62(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=None,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_63(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=None,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_64(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=None,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_65(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=None,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_66(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=None,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_67(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=None,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_68(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_69(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_70(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_71(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_72(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_73(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_74(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug(None)

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_75(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("XX📜🔑✅ Reconstructed CertificateBase from loaded certXX")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_76(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ reconstructed certificatebase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_77(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ RECONSTRUCTED CERTIFICATEBASE FROM LOADED CERT")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_78(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            None,
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_79(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra=None,
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_80(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_81(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_82(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(None).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_83(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"XXerrorXX": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_84(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"ERROR": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_85(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(None), "trace": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_86(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "XXtraceXX": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_87(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "TRACE": traceback.format_exc()},
        )
        raise CertificateError(f"Failed to initialize certificate. Original error: {type(e).__name__}") from e


def x_load_certificate_from_pem__mutmut_88(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(None) from e


def x_load_certificate_from_pem__mutmut_89(
    cert_pem_or_uri: str,
    key_pem_or_uri: str | None = None,
) -> tuple[
    CertificateBase,
    x509.Certificate,
    rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey | None,
    str,
    str | None,
]:
    """Load a certificate and optionally its private key from PEM data or file URIs.

    Returns:
        Tuple of (CertificateBase, X509Certificate, private_key, cert_pem, key_pem)

    """
    try:
        logger.debug("📜🔑🚀 Loading certificate from provided data")
        cert_data = load_from_uri_or_pem(cert_pem_or_uri)

        logger.debug("📜🔑🔍 Loading X.509 certificate from PEM data")
        x509_cert = x509.load_pem_x509_certificate(cert_data.encode("utf-8"))
        logger.debug("📜🔑✅ X.509 certificate object loaded from PEM")

        private_key = None
        key_data = None

        if key_pem_or_uri:
            logger.debug("📜🔑🚀 Loading private key")
            key_data = load_from_uri_or_pem(key_pem_or_uri)

            loaded_priv_key = load_pem_private_key(key_data.encode("utf-8"), password=None)
            if not isinstance(
                loaded_priv_key,
                rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey,
            ):
                raise CertificateError(
                    f"Loaded private key is of unsupported type: {type(loaded_priv_key)}. "
                    "Expected RSA or ECDSA private key.",
                )
            private_key = loaded_priv_key
            logger.debug("📜🔑✅ Private key object loaded and type validated")

        # Extract certificate details for CertificateBase
        loaded_not_valid_before = x509_cert.not_valid_before_utc  # type: ignore[attr-defined]
        loaded_not_valid_after = x509_cert.not_valid_after_utc  # type: ignore[attr-defined]
        if loaded_not_valid_before.tzinfo is None:
            loaded_not_valid_before = loaded_not_valid_before.replace(tzinfo=UTC)
        if loaded_not_valid_after.tzinfo is None:
            loaded_not_valid_after = loaded_not_valid_after.replace(tzinfo=UTC)

        cert_public_key = x509_cert.public_key()
        if not isinstance(cert_public_key, rsa.RSAPublicKey | ec.EllipticCurvePublicKey):
            raise CertificateError(
                f"Certificate's public key is of unsupported type: {type(cert_public_key)}. "
                "Expected RSA or ECDSA public key.",
            )

        base = CertificateBase(
            subject=x509_cert.subject,
            issuer=x509_cert.issuer,
            public_key=cert_public_key,
            not_valid_before=loaded_not_valid_before,
            not_valid_after=loaded_not_valid_after,
            serial_number=x509_cert.serial_number,
        )
        logger.debug("📜🔑✅ Reconstructed CertificateBase from loaded cert")

        return base, x509_cert, private_key, cert_data, key_data

    except Exception as e:
        logger.error(
            f"📜❌ Failed to load certificate. Error: {type(e).__name__}: {e}",
            extra={"error": str(e), "trace": traceback.format_exc()},
        )
        raise CertificateError(
            f"Failed to initialize certificate. Original error: {type(None).__name__}"
        ) from e


x_load_certificate_from_pem__mutmut_mutants: ClassVar[MutantDict] = {
    "x_load_certificate_from_pem__mutmut_1": x_load_certificate_from_pem__mutmut_1,
    "x_load_certificate_from_pem__mutmut_2": x_load_certificate_from_pem__mutmut_2,
    "x_load_certificate_from_pem__mutmut_3": x_load_certificate_from_pem__mutmut_3,
    "x_load_certificate_from_pem__mutmut_4": x_load_certificate_from_pem__mutmut_4,
    "x_load_certificate_from_pem__mutmut_5": x_load_certificate_from_pem__mutmut_5,
    "x_load_certificate_from_pem__mutmut_6": x_load_certificate_from_pem__mutmut_6,
    "x_load_certificate_from_pem__mutmut_7": x_load_certificate_from_pem__mutmut_7,
    "x_load_certificate_from_pem__mutmut_8": x_load_certificate_from_pem__mutmut_8,
    "x_load_certificate_from_pem__mutmut_9": x_load_certificate_from_pem__mutmut_9,
    "x_load_certificate_from_pem__mutmut_10": x_load_certificate_from_pem__mutmut_10,
    "x_load_certificate_from_pem__mutmut_11": x_load_certificate_from_pem__mutmut_11,
    "x_load_certificate_from_pem__mutmut_12": x_load_certificate_from_pem__mutmut_12,
    "x_load_certificate_from_pem__mutmut_13": x_load_certificate_from_pem__mutmut_13,
    "x_load_certificate_from_pem__mutmut_14": x_load_certificate_from_pem__mutmut_14,
    "x_load_certificate_from_pem__mutmut_15": x_load_certificate_from_pem__mutmut_15,
    "x_load_certificate_from_pem__mutmut_16": x_load_certificate_from_pem__mutmut_16,
    "x_load_certificate_from_pem__mutmut_17": x_load_certificate_from_pem__mutmut_17,
    "x_load_certificate_from_pem__mutmut_18": x_load_certificate_from_pem__mutmut_18,
    "x_load_certificate_from_pem__mutmut_19": x_load_certificate_from_pem__mutmut_19,
    "x_load_certificate_from_pem__mutmut_20": x_load_certificate_from_pem__mutmut_20,
    "x_load_certificate_from_pem__mutmut_21": x_load_certificate_from_pem__mutmut_21,
    "x_load_certificate_from_pem__mutmut_22": x_load_certificate_from_pem__mutmut_22,
    "x_load_certificate_from_pem__mutmut_23": x_load_certificate_from_pem__mutmut_23,
    "x_load_certificate_from_pem__mutmut_24": x_load_certificate_from_pem__mutmut_24,
    "x_load_certificate_from_pem__mutmut_25": x_load_certificate_from_pem__mutmut_25,
    "x_load_certificate_from_pem__mutmut_26": x_load_certificate_from_pem__mutmut_26,
    "x_load_certificate_from_pem__mutmut_27": x_load_certificate_from_pem__mutmut_27,
    "x_load_certificate_from_pem__mutmut_28": x_load_certificate_from_pem__mutmut_28,
    "x_load_certificate_from_pem__mutmut_29": x_load_certificate_from_pem__mutmut_29,
    "x_load_certificate_from_pem__mutmut_30": x_load_certificate_from_pem__mutmut_30,
    "x_load_certificate_from_pem__mutmut_31": x_load_certificate_from_pem__mutmut_31,
    "x_load_certificate_from_pem__mutmut_32": x_load_certificate_from_pem__mutmut_32,
    "x_load_certificate_from_pem__mutmut_33": x_load_certificate_from_pem__mutmut_33,
    "x_load_certificate_from_pem__mutmut_34": x_load_certificate_from_pem__mutmut_34,
    "x_load_certificate_from_pem__mutmut_35": x_load_certificate_from_pem__mutmut_35,
    "x_load_certificate_from_pem__mutmut_36": x_load_certificate_from_pem__mutmut_36,
    "x_load_certificate_from_pem__mutmut_37": x_load_certificate_from_pem__mutmut_37,
    "x_load_certificate_from_pem__mutmut_38": x_load_certificate_from_pem__mutmut_38,
    "x_load_certificate_from_pem__mutmut_39": x_load_certificate_from_pem__mutmut_39,
    "x_load_certificate_from_pem__mutmut_40": x_load_certificate_from_pem__mutmut_40,
    "x_load_certificate_from_pem__mutmut_41": x_load_certificate_from_pem__mutmut_41,
    "x_load_certificate_from_pem__mutmut_42": x_load_certificate_from_pem__mutmut_42,
    "x_load_certificate_from_pem__mutmut_43": x_load_certificate_from_pem__mutmut_43,
    "x_load_certificate_from_pem__mutmut_44": x_load_certificate_from_pem__mutmut_44,
    "x_load_certificate_from_pem__mutmut_45": x_load_certificate_from_pem__mutmut_45,
    "x_load_certificate_from_pem__mutmut_46": x_load_certificate_from_pem__mutmut_46,
    "x_load_certificate_from_pem__mutmut_47": x_load_certificate_from_pem__mutmut_47,
    "x_load_certificate_from_pem__mutmut_48": x_load_certificate_from_pem__mutmut_48,
    "x_load_certificate_from_pem__mutmut_49": x_load_certificate_from_pem__mutmut_49,
    "x_load_certificate_from_pem__mutmut_50": x_load_certificate_from_pem__mutmut_50,
    "x_load_certificate_from_pem__mutmut_51": x_load_certificate_from_pem__mutmut_51,
    "x_load_certificate_from_pem__mutmut_52": x_load_certificate_from_pem__mutmut_52,
    "x_load_certificate_from_pem__mutmut_53": x_load_certificate_from_pem__mutmut_53,
    "x_load_certificate_from_pem__mutmut_54": x_load_certificate_from_pem__mutmut_54,
    "x_load_certificate_from_pem__mutmut_55": x_load_certificate_from_pem__mutmut_55,
    "x_load_certificate_from_pem__mutmut_56": x_load_certificate_from_pem__mutmut_56,
    "x_load_certificate_from_pem__mutmut_57": x_load_certificate_from_pem__mutmut_57,
    "x_load_certificate_from_pem__mutmut_58": x_load_certificate_from_pem__mutmut_58,
    "x_load_certificate_from_pem__mutmut_59": x_load_certificate_from_pem__mutmut_59,
    "x_load_certificate_from_pem__mutmut_60": x_load_certificate_from_pem__mutmut_60,
    "x_load_certificate_from_pem__mutmut_61": x_load_certificate_from_pem__mutmut_61,
    "x_load_certificate_from_pem__mutmut_62": x_load_certificate_from_pem__mutmut_62,
    "x_load_certificate_from_pem__mutmut_63": x_load_certificate_from_pem__mutmut_63,
    "x_load_certificate_from_pem__mutmut_64": x_load_certificate_from_pem__mutmut_64,
    "x_load_certificate_from_pem__mutmut_65": x_load_certificate_from_pem__mutmut_65,
    "x_load_certificate_from_pem__mutmut_66": x_load_certificate_from_pem__mutmut_66,
    "x_load_certificate_from_pem__mutmut_67": x_load_certificate_from_pem__mutmut_67,
    "x_load_certificate_from_pem__mutmut_68": x_load_certificate_from_pem__mutmut_68,
    "x_load_certificate_from_pem__mutmut_69": x_load_certificate_from_pem__mutmut_69,
    "x_load_certificate_from_pem__mutmut_70": x_load_certificate_from_pem__mutmut_70,
    "x_load_certificate_from_pem__mutmut_71": x_load_certificate_from_pem__mutmut_71,
    "x_load_certificate_from_pem__mutmut_72": x_load_certificate_from_pem__mutmut_72,
    "x_load_certificate_from_pem__mutmut_73": x_load_certificate_from_pem__mutmut_73,
    "x_load_certificate_from_pem__mutmut_74": x_load_certificate_from_pem__mutmut_74,
    "x_load_certificate_from_pem__mutmut_75": x_load_certificate_from_pem__mutmut_75,
    "x_load_certificate_from_pem__mutmut_76": x_load_certificate_from_pem__mutmut_76,
    "x_load_certificate_from_pem__mutmut_77": x_load_certificate_from_pem__mutmut_77,
    "x_load_certificate_from_pem__mutmut_78": x_load_certificate_from_pem__mutmut_78,
    "x_load_certificate_from_pem__mutmut_79": x_load_certificate_from_pem__mutmut_79,
    "x_load_certificate_from_pem__mutmut_80": x_load_certificate_from_pem__mutmut_80,
    "x_load_certificate_from_pem__mutmut_81": x_load_certificate_from_pem__mutmut_81,
    "x_load_certificate_from_pem__mutmut_82": x_load_certificate_from_pem__mutmut_82,
    "x_load_certificate_from_pem__mutmut_83": x_load_certificate_from_pem__mutmut_83,
    "x_load_certificate_from_pem__mutmut_84": x_load_certificate_from_pem__mutmut_84,
    "x_load_certificate_from_pem__mutmut_85": x_load_certificate_from_pem__mutmut_85,
    "x_load_certificate_from_pem__mutmut_86": x_load_certificate_from_pem__mutmut_86,
    "x_load_certificate_from_pem__mutmut_87": x_load_certificate_from_pem__mutmut_87,
    "x_load_certificate_from_pem__mutmut_88": x_load_certificate_from_pem__mutmut_88,
    "x_load_certificate_from_pem__mutmut_89": x_load_certificate_from_pem__mutmut_89,
}


def load_certificate_from_pem(*args, **kwargs):
    result = _mutmut_trampoline(
        x_load_certificate_from_pem__mutmut_orig, x_load_certificate_from_pem__mutmut_mutants, args, kwargs
    )
    return result


load_certificate_from_pem.__signature__ = _mutmut_signature(x_load_certificate_from_pem__mutmut_orig)
x_load_certificate_from_pem__mutmut_orig.__name__ = "x_load_certificate_from_pem"


# <3 🧱🤝🔒🪄
