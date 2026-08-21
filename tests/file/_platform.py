#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Markers for behaviour that only one family of platforms can exhibit.

Kept in one place so the reason is written once and every test that skips for it
points at the same explanation, rather than each carrying its own paraphrase.
"""

from __future__ import annotations

import sys

import pytest

# Windows has no POSIX mode bits. `os.chmod` there sets or clears a single
# read-only flag and ignores everything else, so a file written with mode 0o600
# reports 0o666 (or 0o444 when read-only), there is nothing to "preserve" across
# a replace, and "not group readable" is not a property the filesystem can
# express at all.
#
# This is a real limit on what Foundation can promise, not a test artefact:
# `atomic_write(..., mode=0o600)` cannot restrict access to the owner on
# Windows. Restricting it there means writing an ACL, which is a feature rather
# than a fix, so these tests skip and the limitation is stated rather than
# quietly asserted away. pyvider makes the same call for its state-store
# equivalent.
requires_posix_permissions = pytest.mark.skipif(
    sys.platform == "win32",
    reason=(
        "POSIX mode bits: Windows chmod only toggles a read-only flag, so owner-only "
        "permissions and mode preservation are not expressible there"
    ),
)

# Windows keeps a mandatory lock on an open file, so `os.replace` onto a path
# another handle still holds fails with PermissionError rather than succeeding
# atomically the way it does on POSIX.
requires_posix_replace_semantics = pytest.mark.skipif(
    sys.platform == "win32",
    reason=(
        "Windows refuses to replace a file another process holds open, so a concurrent "
        "replace raises PermissionError instead of succeeding atomically"
    ),
)


# 🐍🏗️🔚
