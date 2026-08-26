#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Download a published version's artifacts from PyPI, verifying each digest.

Used by the release workflow's repair path. A release whose sign-and-upload
step failed has no artifacts attached, and they cannot be recovered by
rebuilding: the tag's tree and today's tree are not the same, so a rebuild
produces bytes that were never published under that version. Attaching those
would be worse than attaching nothing. PyPI holds the bytes that actually
shipped, and its own sha256 digests are checked here before anything is
written.

Usage: fetch_pypi_artifacts.py <package> <version> <out-dir>
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.request

TIMEOUT = 60


def fail(message: str) -> None:
    print(f"::error::{message}")
    raise SystemExit(1)


def fetch(url: str) -> bytes:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            # Bound to a typed name: urlopen's read() is Any in typeshed, and
            # returning it directly trips mypy's no-any-return under strict.
            payload: bytes = response.read()
        return payload
    except urllib.error.HTTPError as exc:
        fail(f"{url} returned HTTP {exc.code}")
    except Exception as exc:  # network, DNS, TLS
        fail(f"{url} failed: {exc}")
    raise AssertionError("unreachable")


def main(package: str, version: str, out_dir: str) -> None:
    version = version.removeprefix("v")
    meta = json.loads(fetch(f"https://pypi.org/pypi/{package}/{version}/json"))
    files = meta.get("urls") or []
    if not files:
        fail(f"{package} {version} has no files on PyPI")

    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    for entry in files:
        blob = fetch(entry["url"])
        expected = entry["digests"]["sha256"]
        actual = hashlib.sha256(blob).hexdigest()
        if actual != expected:
            fail(f"{entry['filename']}: sha256 {actual} != PyPI's {expected}")
        (out / entry["filename"]).write_bytes(blob)
        print(f"{entry['filename']} ({len(blob)} bytes) sha256 {actual} verified")

    kinds = {p.suffix for p in out.iterdir()}
    if ".whl" not in kinds:
        fail(f"{package} {version} produced no wheel")
    print(f"{len(files)} artifacts for {package} {version} verified against PyPI")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: fetch_pypi_artifacts.py <package> <version> <out-dir>")
    main(sys.argv[1], sys.argv[2], sys.argv[3])
