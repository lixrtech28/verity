"""Deterministic, inspectable research bundles.

A bundle is a directory of canonical JSON artifacts plus a manifest containing
SHA-256 hashes. No generated timestamp or machine-specific path is included,
so identical inputs produce identical artifact hashes.
"""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from typing import Mapping


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_manifest(artifacts: Mapping[str, object]) -> dict:
    files: dict[str, dict[str, object]] = {}
    for name in sorted(artifacts):
        payload = canonical_json(artifacts[name])
        files[name] = {"sha256": sha256_text(payload), "bytes": len(payload.encode("utf-8"))}
    return {"format": "verity.bundle.v1", "files": files}


def write_bundle(output_dir: str | Path, artifacts: Mapping[str, object]) -> Path:
    """Write canonical JSON artifacts and a deterministic manifest."""
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(artifacts)
    for name in sorted(artifacts):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(canonical_json(artifacts[name]), encoding="utf-8")
    (root / "manifest.json").write_text(canonical_json(manifest), encoding="utf-8")
    return root


def bundle_hash(artifacts: Mapping[str, object]) -> str:
    """Return a stable hash of the manifest, useful for reproducibility checks."""
    return sha256_text(canonical_json(build_manifest(artifacts)))
