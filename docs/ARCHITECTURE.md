# VERITY Architecture

## Core pipeline

```text
approved input
    ↓
Evidence records
    ↓
Deterministic extraction
    ↓
Claim records + provenance
    ↓
Evaluation / contradiction layer
    ↓
Optional model-assisted hypotheses
    ↓
Human review
    ↓
Decision artifact
```

## Evidence boundary

An `Evidence` record is an input that a caller has approved for analysis. VERITY does not claim that the underlying source is truthful; it preserves the provenance needed to inspect it.

## Claim boundary

A `Claim` is an observed text fragment selected by the deterministic core. Its ID is derived from source identity and content so repeated processing is stable.

## Hypothesis boundary

Hypotheses are generated interpretations. They are deliberately stored separately from claims and are never silently promoted to facts.

## Future graph

The next major component is a graph connecting claims to evidence, claims to counterclaims, and hypotheses to their supporting assumptions. That graph should make disagreement and uncertainty first-class rather than flattening them into a single confidence number.
