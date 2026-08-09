import json

from verity import build_manifest, bundle_hash, write_bundle


def test_manifest_is_deterministic(tmp_path):
    artifacts = {
        "claims.json": {"claims": [{"id": "c1", "text": "A"}]},
        "graph.json": {"relations": []},
    }

    manifest_a = build_manifest(artifacts)
    manifest_b = build_manifest(dict(reversed(list(artifacts.items()))))

    assert manifest_a == manifest_b
    assert bundle_hash(artifacts) == bundle_hash(dict(reversed(list(artifacts.items()))))

    root = write_bundle(tmp_path / "bundle", artifacts)
    assert json.loads((root / "manifest.json").read_text()) == manifest_a
    assert (root / "claims.json").exists()
    assert (root / "graph.json").exists()
