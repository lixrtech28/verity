# Opportunity Intelligence Agent

A local-first, evidence-disciplined agent that converts a human-approved set of public company sources into supported facts, labeled hypotheses, respectful outreach drafts, discovery questions, and an explicit human-approval record.

## Current build

The first executable module extracts explicit pain signals from approved source text while preserving source URLs and labeling generated opportunities as hypotheses. Nothing is presented as verified without human approval.

### Run

```bash
python -m src.opportunity_intelligence <<'JSON'
{"sources":[{"url":"https://example.com","title":"Example","text":"Teams report a manual reporting process."}]}
JSON
```

### Test

```bash
python -m pytest -q
```

## Design principles

- Public, human-approved sources only.
- Evidence stays attached to findings.
- Facts and hypotheses remain separate.
- Generated conclusions require human approval.
- Local-first execution for the core extraction pipeline.

## Roadmap

1. Source normalization and deduplication.
2. Claim/evidence records with provenance.
3. Contradiction detection.
4. Opportunity scoring with explicit assumptions.
5. Reviewable outreach and discovery artifacts.
6. Provider adapters behind explicit interfaces.
