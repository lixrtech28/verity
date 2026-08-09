# VERITY

### Evidence infrastructure for auditable AI research

VERITY turns research inputs into **traceable claims, explicit evidence, relationship graphs, transparent quality signals, deterministic evaluation reports, and reproducible research bundles**.

> **Evidence first. Inference second. Action only after review.**

AI agents are becoming extremely good at finding and synthesizing information. The weak point is auditability: a fluent answer can hide unsupported claims, lost provenance, contradictory sources, and inference presented as fact.

VERITY is a small, provider-neutral foundation for solving that problem.

## Pipeline

```text
research inputs
      ↓
normalized evidence
      ↓
atomic claims ─────────────┐
      ↓                    │
provenance                 │
      ↓                    │
quality signals            │
      ↓                    │
relationship graph ←───────┘
      ↓
structural evaluation
      ↓
reproducible bundle
      ↓
human review
      ↓
decision artifacts
```

The core is deterministic and works without an LLM or hosted service.

## What is implemented

### Traceable claims

Every extracted claim gets a stable content-derived ID and retains its source ID and URL.

### Evidence graph

`EvidenceGraph` stores explicit relationships:

- `supports`
- `contradicts`
- `derived_from`
- `related_to`

VERITY does not silently infer truth from an edge. Relationships remain explicit and reviewable.

### Transparent quality scoring

`score_evidence()` exposes structural signals for completeness, specificity, and provenance. It is a heuristic, not a truth detector.

### Deterministic evaluation

`evaluate()` checks structural integrity across evidence, claims, and graph relationships. It reports:

- missing source references
- unknown graph nodes
- low-quality sources
- explicit contradictions
- claims without support/derivation edges

The result is `pass`, `review`, or `fail`. A `review` result is not a claim that the research is false; it means a human should inspect the flagged conditions.

### Reproducible research bundles

`write_bundle()` writes canonical JSON artifacts plus a manifest containing SHA-256 hashes. The format intentionally excludes machine-specific paths and generated timestamps so identical inputs produce stable artifact hashes.

```text
bundle/
├── evidence.json
├── claims.json
├── graph.json
├── quality.json       # optional
├── evaluation.json    # optional
└── manifest.json
```

See [`docs/RESEARCH_BUNDLES.md`](docs/RESEARCH_BUNDLES.md).

### JSONL streaming

Evidence can be read from and written to JSONL for batch pipelines and agent workflows without requiring a database or hosted service.

### CLI

```bash
# Build claims
verity examples/demo.json

# Include quality signals
verity examples/demo.json --quality

# Evaluate the evidence graph
verity examples/demo.json --quality --evaluate

# Produce a reproducible bundle
verity examples/demo.json --quality --evaluate --bundle ./bundle
```

## Quick start

Requires Python 3.11+.

```bash
pip install -e .
verity examples/demo.json --quality --evaluate
```

Or use the library directly:

```python
from verity import Evidence, EvidenceGraph, Relation, build_claims, evaluate

item = Evidence(
    source_id="source-1",
    url="https://example.com/report",
    title="Example report",
    text="Customers report that weekly reporting takes hours of manual work.",
)

result = build_claims([item])
graph = EvidenceGraph([Relation("source-1", result.claims[0].claim_id, "supports")])

print(evaluate([item], result.claims, graph).to_json())
```

Run the test suite:

```bash
python -m pytest -q
```

## Why this exists

The next generation of research will increasingly be performed by agents. That makes the primitive underneath the agent important: **can another person inspect why the system believes something?**

VERITY is an experiment in making that primitive open, small, composable, and auditable.

## Design principles

- **Provenance is data.** Every claim points back to its source.
- **Claims are not hypotheses.** Observation and interpretation are separate.
- **Relationships are explicit.** Support and contradiction are recorded, not hidden inside prose.
- **Evaluation is structural.** The evaluator finds integrity problems; it does not pretend to establish truth.
- **Scores are inspectable.** Heuristics expose their assumptions.
- **Models are replaceable.** LLMs can assist; they are not the source of truth.
- **Human review is explicit.** The library never silently takes external action.
- **Reproducibility matters.** Canonical artifacts and hashes make research packages inspectable.
- **Security is part of research integrity.** No covert collection, access-control bypassing, fabricated respondents, or synthetic evidence presented as human evidence.

## Roadmap

- [x] Evidence and claim data model
- [x] Stable content-derived identifiers
- [x] Provenance-preserving extraction
- [x] Fact / hypothesis separation
- [x] Deterministic CLI
- [x] Evidence relationship graph
- [x] Explicit evidence-quality signals
- [x] JSONL streaming interface
- [x] Structural evaluation engine
- [x] Reproducible research bundles
- [x] Tests and CI
- [ ] Claim-to-claim semantic contradiction detection
- [ ] Pluggable LLM adapters with provenance-preserving outputs
- [ ] Public evaluation suite for provenance and extraction accuracy
- [ ] GitHub Action for evidence checks
- [ ] Adapters for common research-agent frameworks

## Project status

**Early-stage open source.** The project favors small deterministic primitives over a large opaque agent framework.

Contributions, criticism, reproducible examples, and failure cases are welcome.

## License

MIT.
