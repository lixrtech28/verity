"""VERITY: evidence infrastructure for auditable AI research."""

from .bundle import build_manifest, bundle_hash, canonical_json, write_bundle
from .core import Claim, Evidence, ResearchResult, build_claims
from .evaluate import EvaluationReport, Finding, evaluate
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
    "Finding",
    "EvaluationReport",
    "evaluate",
    "canonical_json",
    "build_manifest",
    "bundle_hash",
    "write_bundle",
    "evidence_from_jsonl",
    "evidence_to_jsonl",
]
