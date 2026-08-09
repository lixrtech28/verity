# VERITY

### Evidence infrastructure for AI research

VERITY turns research inputs into **traceable claims, explicit evidence, separated hypotheses, relationship graphs, transparent quality signals, and reviewable decisions**.

> **Evidence first. Inference second. Action only after review.**

AI agents are becoming extremely good at finding and synthesizing information. The weak point is auditability: a fluent answer can hide unsupported claims, lost provenance, contradictory sources, and inference presented as fact.

VERITY is a small, provider-neutral foundation for solving that problem.

## Pipeline

```text
research inputs
      ↓
normalized evidence
      ↓
atomic claims ────────┐
      ↓                │
provenance             │
      ↓                │
quality signals        │
      ↓                │
relationship graph ←───┘
  │       │
  │       └── supports / contradicts / derived_from
  ↓
hypotheses
      ↓
human review
      ↓
decision artifacts
```

The core is deterministic and works without an LLM or hosted service.

## What is implemented

### 1. Traceable claims

Every extracted claim gets a stable content-derived ID and retains its source ID and URL. This makes downstream records referential instead of relying on model-generated labels.

### 2. Evidence graph

`EvidenceGraph` stores explicit relationships between research objects:

- `supports`
- `contradicts`
- `derived_from`
- `related_to`

VERITY does not silently infer truth from a graph edge. Relationships are explicit inputs that can be reviewed or produced by a separate evaluation/model layer.

### 3. Transparent quality scoring

`score_evidence()` exposes structural signals for completeness, specificity, and provenance. The score is deliberately a heuristic, not a truth detector. Every component and rationale is inspectable and replaceable.

### 4. JSONL streaming

Evidence can be read from and written to JSONL for batch pipelines and agent workflows without requiring a database or hosted service.

### 5. Deterministic CLI

```bash
# JSON evidence document
verity examples/demo.json

# JSONL evidence stream
verity evidence.jsonl --jsonl

# Include transparent quality signals
verity examples/demo.json --quality
```

### 6. Human-review boundary

The library does not silently take external actions. Model adapters and automation can be layered on top, but the evidence model remains inspectable.

## Quick start

Requires Python 3.11+.

```bash
pip install -e .
verity examples/demo.json --quality
```

Or use the library directly:

```python
from verity import Evidence, build_claims, score_evidence

item = Evidence(
    source_id="source-1",
    url="https://example.com/report",
    title="Example report",
    text="Customers report that weekly reporting takes hours of manual work.",
)

result = build_claims([item])
print(result.to_json())
print(score_evidence(item).to_json())
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
- **Claims are not hypotheses.** Observed evidence and interpretation are separate types.
- **Relationships are explicit.** A contradiction or support edge is recorded, not hidden inside prose.
- **Scores are inspectable.** Heuristics expose their assumptions instead of pretending to be certainty.
- **Models are replaceable.** LLMs can assist; they are not the source of truth.
- **Human review is explicit.** The library never silently takes external action.
- **Reproducibility matters.** Inputs, outputs, IDs, and assumptions should be inspectable.
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
- [x] Tests and CI
- [ ] Claim-to-claim contradiction detection
- [ ] Pluggable LLM adapters with provenance-preserving outputs
- [ ] Public evaluation suite for provenance and extraction accuracy
- [ ] GitHub Action for evidence checks
- [ ] Adapters for common research-agent frameworks
- [ ] Versioned evidence snapshots and reproducible research bundles

## Project status

**Early-stage open source.** The data model is being developed in public. The project favors small deterministic primitives over a large opaque agent framework.

Contributions, criticism, reproducible examples, and failure cases are welcome.

## License

MIT.
