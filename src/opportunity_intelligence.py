"""Small, deterministic evidence layer for research-oriented AI systems."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
import sys
from typing import Iterable


@dataclass(frozen=True)
class Source:
    url: str
    title: str
    text: str


@dataclass(frozen=True)
class Finding:
    id: str
    text: str
    kind: str
    source_url: str
    source_title: str
    confidence: float


PAIN_TERMS = re.compile(
    r"\b(problem|pain|manual|slow|expensive|difficult|frustrat|broken|"
    r"inefficient|spreadsheet|workaround|missing|complain|wish)\w*\b",
    re.I,
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _finding_id(source: Source, sentence: str) -> str:
    payload = f"{source.url}\n{_normalize(sentence)}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def extract_findings(sources: Iterable[Source]) -> list[Finding]:
    """Extract deterministic pain signals while preserving provenance."""
    findings: list[Finding] = []
    seen: set[str] = set()

    for source in sources:
        for raw_sentence in re.split(r"(?<=[.!?])\s+", source.text.strip()):
            sentence = _normalize(raw_sentence)
            if not sentence or not PAIN_TERMS.search(sentence):
                continue

            finding_id = _finding_id(source, sentence)
            if finding_id in seen:
                continue
            seen.add(finding_id)

            findings.append(
                Finding(
                    id=finding_id,
                    text=sentence,
                    kind="pain_signal",
                    source_url=source.url,
                    source_title=source.title,
                    confidence=0.5,
                )
            )

    return findings


def build_report(sources: Iterable[Source]) -> dict:
    """Build a traceable report; hypotheses remain explicitly unverified."""
    source_list = list(sources)
    findings = extract_findings(source_list)

    return {
        "schema_version": "0.2",
        "sources": [asdict(source) for source in source_list],
        "findings": [
            {
                **asdict(finding),
                "evidence": {"url": finding.source_url, "title": finding.source_title},
            }
            for finding in findings
        ],
        "hypotheses": [
            {
                "id": f"hyp-{finding.id}",
                "text": f"This signal may indicate an opportunity: {finding.text}",
                "status": "hypothesis",
                "based_on": [finding.id],
            }
            for finding in findings
        ],
        "human_approval_required": True,
    }


def main() -> None:
    payload = json.load(sys.stdin)
    sources = [Source(**item) for item in payload.get("sources", [])]
    print(json.dumps(build_report(sources), indent=2))


if __name__ == "__main__":
    main()
