"""Fetch the Teamleader Focus OpenAPI spec from the npm registry.

Downloads the ``@teamleader/focus-api-specification`` package tarball
directly over HTTP (no npm CLI required), extracts the dereferenced
YAML spec, caches it to ``codegen/spec/api.yaml``, and returns the
parsed dict plus the spec version string.
"""

from __future__ import annotations

import io
import tarfile
from pathlib import Path
from typing import Any

import requests
import yaml

NPM_REGISTRY_URL = (
    "https://registry.npmjs.org/@teamleader/focus-api-specification/latest"
)
SPEC_FILENAME_IN_TARBALL = "package/dist/api.focus.teamleader.eu.dereferenced.yaml"
SPEC_CACHE_PATH = Path(__file__).parent / "spec" / "api.yaml"


def fetch_spec() -> tuple[dict[str, Any], str]:
    """Return ``(spec_dict, version_string)``.

    Side-effect: writes the raw YAML to ``codegen/spec/api.yaml``.
    """
    print("Fetching spec metadata from npm registry …")
    meta_resp = requests.get(NPM_REGISTRY_URL, timeout=30)
    meta_resp.raise_for_status()
    meta = meta_resp.json()

    version: str = meta["version"]
    tarball_url: str = meta["dist"]["tarball"]
    print(f"  version    : {version}")
    print(f"  tarball    : {tarball_url}")

    print("Downloading tarball …")
    tarball_resp = requests.get(tarball_url, timeout=120)
    tarball_resp.raise_for_status()

    print("Extracting YAML …")
    with tarfile.open(fileobj=io.BytesIO(tarball_resp.content), mode="r:gz") as tar:
        try:
            member = tar.getmember(SPEC_FILENAME_IN_TARBALL)
        except KeyError:
            available = [m.name for m in tar.getmembers() if m.name.endswith(".yaml")]
            raise RuntimeError(
                f"Could not find {SPEC_FILENAME_IN_TARBALL!r} in tarball.\n"
                f"Available YAML files: {available}"
            )
        f = tar.extractfile(member)
        if f is None:
            raise RuntimeError(f"Could not read {SPEC_FILENAME_IN_TARBALL!r}")
        raw_yaml = f.read()

    SPEC_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPEC_CACHE_PATH.write_bytes(raw_yaml)
    print(f"  cached to  : {SPEC_CACHE_PATH}")

    spec: dict[str, Any] = yaml.safe_load(raw_yaml)
    return spec, version
