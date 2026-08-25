#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Generate a CycloneDX SBOM for the *built wheel and its dependencies*.
#
# `cyclonedx-py environment` describes whatever is installed in an interpreter,
# so run bare under `uvx` it described the ephemeral tool venv -- cyclonedx-bom
# and its own dependencies, nothing of this package. The wheel is installed into
# a fresh venv here and that venv's interpreter is the one described.
#
# That mistake published 77 SBOMs across this ecosystem, every one listing the
# same 34 packages and none of them the release they claimed to describe. It is
# worse than shipping nothing: a CVE sweep querying it gets a confident wrong
# answer. The check at the end exists so it cannot happen quietly again.
#
# Usage: scripts/sbom_from_wheel.sh <dist-dir> <output-file>
set -euo pipefail

# Pinned: this runs code fetched from PyPI inside the release workflow. Bump
# deliberately, and re-run the script locally against a fresh `uv build` first.
CYCLONEDX_BOM_VERSION="7.3.1"

DIST_DIR="${1:?usage: sbom_from_wheel.sh <dist-dir> <output-file>}"
OUT="${2:?usage: sbom_from_wheel.sh <dist-dir> <output-file>}"

VENV="$(mktemp -d)/sbom-venv"
uv venv --quiet "$VENV"
uv pip install --quiet --python "$VENV/bin/python" "$DIST_DIR"/*.whl
uvx --from "cyclonedx-bom==${CYCLONEDX_BOM_VERSION}" cyclonedx-py environment "$VENV/bin/python" --output-format json -o "$OUT"

# The SBOM must name the package its own wheel filename says it describes.
python3 - "$DIST_DIR" "$OUT" <<'PYEOF'
import json
import pathlib
import sys

dist, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
wheel = next(iter(sorted(dist.glob("*.whl"))), None)
if wheel is None:
    print(f"::error::no wheel in {dist}/ to check the SBOM against")
    raise SystemExit(1)

expected = wheel.name.split("-")[0].replace("_", "-").lower()
names = {c["name"].replace("_", "-").lower() for c in json.loads(out.read_text())["components"]}
if expected not in names:
    print(f"::error::SBOM names {len(names)} packages but not {expected} -- it is describing the wrong environment")
    raise SystemExit(1)
print(f"SBOM names {expected} among {len(names)} components")
PYEOF

echo "SBOM written to $OUT"
