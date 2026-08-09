"""Command-line interface for VERITY."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bundle import write_bundle
from .core import Evidence, build_claims
from .evaluate import evaluate
from .graph import EvidenceGraph, Relation
from .jsonl import evidence_from_jsonl
from .quality import score_evidence


def _load(path: Path, jsonl: bool) -> tuple[list[Evidence], EvidenceGraph]:
    if jsonl:
        return list(evidence_from_jsonl(path.read_text(encoding="utf-8").splitlines())), EvidenceGraph()

    payload = json.loads(path.read_text(encoding="utf-8"))
    evidence = [Evidence(**item) for item in payload.get("evidence", [])]
    relations = [Relation(**item) for item in payload.get("relations", [])]
    return evidence, EvidenceGraph(relations)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build and evaluate traceable claims from approved evidence."
    )
    parser.add_argument("input", type=Path, help="JSON evidence/graph file or JSONL file")
    parser.add_argument("--jsonl", action="store_true", help="Read newline-delimited Evidence records")
    parser.add_argument("--quality", action="store_true", help="Include transparent evidence-quality scores")
    parser.add_argument("--evaluate", action="store_true", help="Run deterministic graph/evidence checks")
    parser.add_argument("--bundle", type=Path, help="Write a reproducible research bundle to this directory")
    args = parser.parse_args()

    evidence, graph = _load(args.input, args.jsonl)
    research = build_claims(evidence)
    result = research.to_dict()
    result["graph"] = graph.to_dict()

    if args.quality:
        result["quality"] = [score_evidence(item).to_dict() for item in evidence]

    if args.evaluate:
        result["evaluation"] = evaluate(evidence, research.claims, graph).to_dict()

    if args.bundle:
        artifacts = {
            "evidence.json": {"evidence": [item.__dict__ for item in evidence]},
            "claims.json": {"claims": [item.__dict__ for item in research.claims], "hypotheses": list(research.hypotheses)},
            "graph.json": graph.to_dict(),
        }
        if args.quality:
            artifacts["quality.json"] = {"quality": [score_evidence(item).to_dict() for item in evidence]}
        if args.evaluate:
            artifacts["evaluation.json"] = evaluate(evidence, research.claims, graph).to_dict()
        write_bundle(args.bundle, artifacts)
        result["bundle"] = str(args.bundle)

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
