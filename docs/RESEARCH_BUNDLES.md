# Reproducible research bundles

A VERITY bundle is a portable snapshot of the evidence state used to produce a research artifact.

## Format

```text
bundle/
├── evidence.json
├── claims.json
├── graph.json
├── quality.json       # optional
├── evaluation.json    # optional
└── manifest.json
```

Every JSON artifact is serialized canonically: UTF-8, sorted object keys, compact separators, and a trailing newline. `manifest.json` records the SHA-256 digest and byte length of every artifact.

## Why the format is deterministic

The bundle writer intentionally excludes generated timestamps, local filesystem paths, hostnames, and random identifiers. If two runs receive identical artifact objects, their artifact hashes and manifest hash are identical.

This makes the bundle useful for:

- regression tests
- research handoffs
- audit trails
- CI checks
- comparing agent runs
- attaching evidence to a decision

## CLI example

```bash
verity examples/demo.json --quality --evaluate --bundle ./bundle
```

The command writes the evidence, extracted claims, relationship graph, quality signals, evaluation report, and manifest when the corresponding flags are enabled.

## What reproducibility does not mean

A stable hash does **not** prove that a source is truthful. It proves that the recorded artifact has not changed. Source validity, sampling quality, interpretation, and domain correctness still require review.
