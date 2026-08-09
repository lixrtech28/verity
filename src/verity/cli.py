"""Command-line interface for VERITY."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import Evidence, build_claims
from .jsonl import evidence_from_jsonl
from .quality import score_evidence


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build traceable claims from approved evidence."
    )
    parser.add_argument("input", type=Path, help="JSON evidence file or JSONL file")
    parser.add_argument(
        "--jsonl", action="store_true", help="Read newline-delimited Evidence records"
    )
    parser.add_argument(
        "--quality", action="store_true", help="Include transparent evidence-quality scores"
    )
    args = parser.parse_args()

    if args.jsonl:
        evidence = list(evidence_from_jsonl(args.input.read_text(encoding="utf-8").splitlines()))
    else:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        evidence = [Evidence(**item) for item in payload.get("evidence", [])]

    result = build_claims(evidence).to_dict()
    if args.quality:
        result["quality"] = [score_evidence(item).to_dict() for item in evidence]
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
