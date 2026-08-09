"""VERITY: evidence infrastructure for auditable AI research."""

from .core import Claim, Evidence, ResearchResult, build_claims
from .graph import EvidenceGraph, Relation
from .jsonl import evidence_from_jsonl, evidence_to_jsonl
from .quality import QualityScore, score_evidence

__all__ = [
    "Claim",
    "Evidence",
    "ResearchResult",
    "build_claims",
    "EvidenceGraph",
    "Relation",
    "QualityScore",
    "score_evidence",
    "evidence_from_jsonl",
    "evidence_to_jsonl",
]
