# Opportunity Intelligence Agent

A local-first, evidence-disciplined research tool for turning a human-approved set of public company sources into traceable opportunity signals.

The project is deliberately built around a simple rule: **evidence first, inference second, action only after human approval.**

## What it does today

The v0.1 core:

- extracts explicit pain signals from approved source text
- preserves source URLs with findings
- separates observed signals from generated hypotheses
- produces reviewable opportunity records
- keeps external actions behind an explicit human-approval boundary
- runs without a model or hosted service in the core extraction path

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

## Why this exists

Market and company research produces large amounts of fragmented public information, but useful opportunities are often buried inside repetitive operational complaints, product friction, workflow descriptions, and buyer language.

This project is an experiment in making that evidence computable without collapsing facts and model-generated interpretation into the same object.

## Architecture direction

```text
approved sources
      ↓
normalization / deduplication
      ↓
source-backed claims
      ↓
contradiction checks
      ↓
opportunity hypotheses
      ↓
human review
      ↓
research / discovery artifacts
```

## Roadmap

1. Source normalization and deduplication.
2. Claim/evidence records with provenance.
3. Contradiction detection.
4. Opportunity scoring with explicit assumptions.
5. Reviewable outreach and discovery artifacts.
6. Provider adapters behind explicit interfaces.
7. Evaluation suite for extraction quality and provenance integrity.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security-sensitive reports should follow [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
