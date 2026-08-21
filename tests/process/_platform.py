#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Markers for process tests written against a POSIX shell.

The feature under test -- passing `cwd`, passing `env`, streaming output -- is
not POSIX-specific, and Foundation supports all of it on Windows. What is
POSIX-specific is how these particular tests *observe* it: they run `pwd` to
report the working directory and `echo $VAR` to report the environment, and
neither means anything to `cmd.exe`, which spells the second `%VAR%` and has no
`pwd` of its own.

Two separate things go wrong on Windows as a result:

* `echo $SHELL_TEST_VAR` is echoed literally rather than expanded, so the
  assertion sees the variable's name where it wanted its value.
* Where the runner does have a `pwd` on PATH (Git Bash ships one), it reports
  the 8.3 short form -- `C:\\Users\\RUNNER~1\\...` -- while the fixture holds the
  long name, so `assert tmpdir in result.stdout` fails on two spellings of the
  same directory.

Skipped rather than rewritten because rewriting them to a portable probe
(`python -c "import os; print(os.getcwd())"`) changes what is being exercised --
a Python subprocess instead of a shell builtin -- and that is a different test,
worth adding deliberately rather than by mechanical substitution. Foundation's
process handling on Windows is therefore *not* covered by CI; that gap is real
and is the follow-up, not something this marker pretends away.
"""

from __future__ import annotations

import sys

import pytest

requires_posix_shell = pytest.mark.skipif(
    sys.platform == "win32",
    reason=(
        "observes the process through `pwd` / `echo $VAR`, which cmd.exe does not "
        "provide or expand; the feature works on Windows, the probe does not"
    ),
)


# 🐍🏗️🔚
