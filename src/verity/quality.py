"""Transparent evidence-quality scoring.

This is deliberately a heuristic, not a truth detector. Every component is
visible so users can replace the policy with domain-specific evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json

from .core import Evidence


@dataclass(frozen=True)
class QualityScore:
    source_id: str
    score: float
    completeness: float
    specificity: float
    provenance: float
    rationale: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


def score_evidence(item: Evidence) -> QualityScore:
    """Score evidence using inspectable structural signals only."""
    reasons: list[str] = []
    completeness = 1.0 if item.text.strip() and item.title.strip() else 0.0
    specificity = min(len(item.text.split()) / 40.0, 1.0)
    provenance = 1.0 if item.source_id.strip() and item.url.startswith(("http://", "https://")) else 0.0

    if completeness == 1.0:
        reasons.append("source has title and non-empty evidence text")
    else:
        reasons.append("source is missing title or evidence text")
    if specificity >= 0.75:
        reasons.append("evidence contains substantial textual detail")
    else:
        reasons.append("evidence is short and may need additional context")
    if provenance == 1.0:
        reasons.append("source identity and URL are present")
    else:
        reasons.append("source provenance is incomplete")

    score = round((completeness + specificity + provenance) / 3.0, 3)
    return QualityScore(item.source_id, score, completeness, specificity, provenance, tuple(reasons))
