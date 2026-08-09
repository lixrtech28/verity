"""Deterministic evaluation checks for evidence-backed research results.

The evaluator reports structural problems. It does not decide whether a
claim is factually true; truth still requires source review and domain judgment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Iterable

from .core import Claim, Evidence
from .graph import EvidenceGraph
from .quality import score_evidence


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    node_id: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class EvaluationReport:
    status: str
    findings: tuple[Finding, ...]
    metrics: dict[str, int | float]

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "findings": [item.to_dict() for item in self.findings],
            "metrics": self.metrics,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, sort_keys=True)


def evaluate(
    evidence: Iterable[Evidence],
    claims: Iterable[Claim],
    graph: EvidenceGraph,
    *,
    minimum_quality: float = 0.25,
) -> EvaluationReport:
    """Run reproducible structural checks over an evidence set."""
    evidence_list = tuple(evidence)
    claims_list = tuple(claims)
    findings: list[Finding] = []

    evidence_ids = {item.source_id for item in evidence_list}
    claim_ids = {item.claim_id for item in claims_list}

    for claim in claims_list:
        if claim.source_id not in evidence_ids:
            findings.append(Finding(
                "MISSING_SOURCE", "error",
                f"claim {claim.claim_id} references unknown source {claim.source_id}",
                claim.claim_id,
            ))

    for item in evidence_list:
        quality = score_evidence(item)
        if quality.score < minimum_quality:
            findings.append(Finding(
                "LOW_QUALITY_SOURCE", "warning",
                f"source {item.source_id} has quality score {quality.score:.3f} below {minimum_quality:.3f}",
                item.source_id,
            ))

    for relation in graph.relations:
        if relation.source not in claim_ids and relation.source not in evidence_ids:
            findings.append(Finding(
                "UNKNOWN_GRAPH_NODE", "error",
                f"graph relation references unknown source node {relation.source}",
                relation.source,
            ))
        if relation.target not in claim_ids and relation.target not in evidence_ids:
            findings.append(Finding(
                "UNKNOWN_GRAPH_NODE", "error",
                f"graph relation references unknown target node {relation.target}",
                relation.target,
            ))

    for relation in graph.contradictions():
        findings.append(Finding(
            "CONTRADICTION", "warning",
            relation.rationale or f"{relation.source} contradicts {relation.target}",
            relation.source,
        ))

    supported_claims = {
        relation.target
        for relation in graph.relations
        if relation.relation in {"supports", "derived_from"}
    }
    for claim in claims_list:
        if claim.claim_id not in supported_claims:
            findings.append(Finding(
                "UNLINKED_CLAIM", "warning",
                f"claim {claim.claim_id} has no explicit support/derivation edge in the graph",
                claim.claim_id,
            ))

    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    status = "fail" if errors else ("review" if warnings else "pass")

    return EvaluationReport(
        status=status,
        findings=tuple(findings),
        metrics={
            "evidence_count": len(evidence_list),
            "claim_count": len(claims_list),
            "relation_count": len(graph.relations),
            "contradiction_count": len(graph.contradictions()),
            "error_count": errors,
            "warning_count": warnings,
        },
    )
