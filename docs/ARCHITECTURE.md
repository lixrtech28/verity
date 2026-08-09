# Architecture

## Purpose

Opportunity Intelligence is a local-first evidence pipeline for turning human-approved public-source text into traceable research signals. It deliberately separates observations from generated hypotheses.

## Pipeline

```text
approved sources
      |
      v
source normalization
      |
      v
atomic findings + provenance
      |
      +----> pain signals
      |
      +----> factual observations
      |
      v
hypothesis generation
      |
      v
human review / approval
      |
      v
exportable research artifact
```

## Non-goals

- No covert collection.
- No bypassing access controls.
- No fabricated respondents or synthetic evidence presented as human evidence.
- No claim is considered verified merely because a model generated it.

## Extension points

Future adapters will sit behind explicit interfaces for source ingestion, retrieval, LLM-assisted extraction, scoring, and export. The core data model should remain provider-neutral so the project can be used with local models, hosted APIs, or deterministic pipelines.

## Why this matters

AI agents can generate plausible research extremely quickly. The harder engineering problem is preserving provenance, separating evidence from inference, detecting contradictions, and making review auditable. This project treats those properties as first-class infrastructure.
