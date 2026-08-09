# VERITY

### Evidence infrastructure for AI research

VERITY turns research inputs into **traceable claims, explicit evidence, separated hypotheses, and reviewable decisions**.

> **Evidence first. Inference second. Action only after review.**

AI agents are becoming extremely good at finding and synthesizing information. The weak point is auditability: a fluent answer can hide unsupported claims, lost provenance, contradictory sources, and inference presented as fact.

VERITY is a small, provider-neutral foundation for solving that problem.

## What VERITY does

```text
research inputs
      ↓
normalized evidence
      ↓
atomic claims
      ↓
provenance
      ↓
contradiction / support checks
      ↓
hypotheses
      ↓
human review
      ↓
decision artifacts
```

The core is deterministic and works without an LLM or hosted service.

### Design principles

- **Provenance is data.** Every claim points back to its source.
- **Claims are not hypotheses.** Observed evidence and interpretation are separate types.
- **Models are replaceable.** LLMs can assist; they are not the source of truth.
- **Human review is explicit.** The library never silently takes external action.
- **Reproducibility matters.** Inputs, outputs, IDs, and assumptions should be inspectable.
- **Security is part of research integrity.** No covert collection, access-control bypassing, fabricated respondents, or synthetic evidence presented as human evidence.

## Quick start

Requires Python 3.11+.

```bash
pip install -e .
verity demo.json
```

Or use the library directly:

```python
from verity import Evidence, build_claims

items = [
    Evidence(
        source_id="source-1",
        url="https://example.com/report",
        title="Example report",
        text="Customers report that weekly reporting takes hours of manual work.",
    )
]

result = build_claims(items)
print(result.to_json())
```

Run the test suite:

```bash
python -m pytest -q
```

## Why this exists

The next generation of research will increasingly be performed by agents. That makes the primitive underneath the agent important: **can another person inspect why the system believes something?**

VERITY is an experiment in making that primitive open, small, composable, and auditable.

## Roadmap

- [x] Evidence and claim data model
- [x] Stable content-derived identifiers
- [x] Provenance-preserving extraction
- [x] Fact / hypothesis separation
- [x] Deterministic CLI
- [x] Tests and CI
- [ ] Claim-to-claim support and contradiction graph
- [ ] Evidence quality scoring with explicit assumptions
- [ ] JSONL streaming interface
- [ ] Pluggable LLM adapters
- [ ] Evaluation suite for provenance and extraction accuracy
- [ ] GitHub Action for evidence checks
- [ ] Adapters for common research-agent frameworks

## Project status

Early-stage open source. The project is intentionally small while the data model and evaluation methodology are developed in public.

Contributions, criticism, reproducible examples, and failure cases are welcome.

## License

MIT.
