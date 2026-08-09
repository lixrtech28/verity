# VERITY — Evidence Graph for AI Research

> **Turn messy public evidence into traceable claims, hypotheses, and decisions.**

VERITY is a local-first, evidence-disciplined research engine for developers building AI agents that need to reason over real-world information without losing provenance.

**Core rule:** evidence first → inference second → human approval before action.

## Why VERITY?

AI can produce a convincing answer in seconds. The difficult engineering problem is knowing **which parts are supported, where the support came from, what is inference, and what still needs verification**.

VERITY treats those concerns as infrastructure.

## What exists today

- Extracts explicit pain signals from approved source text.
- Preserves source URLs and titles with findings.
- Separates observed evidence from generated hypotheses.
- Produces reviewable opportunity records.
- Keeps external actions behind an explicit human-approval boundary.
- Runs the core extraction path without a hosted model or service.
- Includes tests, CI, security guidance, contribution guidance, and a runnable example.

## Quick start

```bash
python -m src.opportunity_intelligence <<'JSON'
{"sources":[{"url":"https://example.com","title":"Example","text":"Teams report a manual reporting process."}]}
JSON
```

Run tests:

```bash
python -m pytest -q
```

See `examples/demo.json` for an input example and `docs/ARCHITECTURE.md` for the design model.

## Architecture

```text
approved sources
      │
      ▼
normalization / deduplication
      │
      ▼
source-backed observations
      │
      ├──────────────┐
      ▼              ▼
  evidence       pain signals
      │              │
      └──────┬───────┘
             ▼
     hypothesis generation
             │
             ▼
      contradiction checks
             │
             ▼
       human review gate
             │
             ▼
       research artifacts
```

## Design principles

### Provenance is data

Every extracted finding should retain enough source context to let a reviewer trace it back to the approved input.

### Facts are not hypotheses

An observed statement and a model-generated opportunity are different objects. VERITY keeps that distinction explicit.

### Models are replaceable

The core data model is provider-neutral. Future LLM adapters can assist extraction or reasoning without becoming the source of truth.

### Human approval is a boundary

The system may prepare research and discovery artifacts, but it does not silently take external actions.

### Security and research integrity are features

No covert collection, access-control bypassing, fabricated respondents, or synthetic evidence presented as human evidence.

## Roadmap

- [x] Evidence-aware extraction core
- [x] Provenance-preserving findings
- [x] Fact / hypothesis separation
- [x] Human approval boundary
- [x] Tests and CI
- [x] Security and contribution documentation
- [x] Runnable example
- [ ] Source normalization and deduplication
- [ ] Claim/evidence graph
- [ ] Contradiction detection
- [ ] Opportunity scoring with explicit assumptions
- [ ] Pluggable LLM adapters
- [ ] Evaluation suite for extraction quality and provenance integrity
- [ ] CLI with structured JSON/JSONL export
- [ ] GitHub Action for evidence checks on research artifacts

## Who it is for

VERITY is aimed at developers, researchers, analysts, and agent builders who need **auditable research rather than merely plausible text**.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security-sensitive reports should follow [SECURITY.md](SECURITY.md). Feature proposals can use `docs/FEATURE_REQUEST.md`.

## License

MIT. See [LICENSE](LICENSE).
