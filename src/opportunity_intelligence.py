"""Evidence-disciplined opportunity extraction from human-approved public sources."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable
import json
import re


@dataclass(frozen=True)
class Source:
    url: str
    title: str
    text: str


@dataclass(frozen=True)
class Finding:
    text: str
    kind: str
    source_url: str
    confidence: float


PAIN_TERMS = re.compile(
    r"\b(problem|pain|manual|slow|expensive|difficult|frustrat|broken|"
    r"inefficient|spreadsheet|workaround|missing|complain|wish)\w*\b",
    re.I,
)


def extract_findings(sources: Iterable[Source]) -> list[Finding]:
    findings: list[Finding] = []
    for source in sources:
        for sentence in re.split(r"(?<=[.!?])\s+", source.text.strip()):
            if not sentence or not PAIN_TERMS.search(sentence):
                continue
            findings.append(
                Finding(
                    text=sentence.strip(),
                    kind="pain_signal",
                    source_url=source.url,
                    confidence=0.5,
                )
            )
    return findings


def build_report(sources: Iterable[Source]) -> dict:
    source_list = list(sources)
    findings = extract_findings(source_list)
    return {
        "sources": [asdict(source) for source in source_list],
        "findings": [asdict(finding) for finding in findings],
        "hypotheses": [
            {
                "text": f"Repeated pain signal may indicate an opportunity: {finding.text}",
                "status": "hypothesis",
                "evidence": finding.source_url,
            }
            for finding in findings
        ],
        "human_approval_required": True,
    }


def main() -> None:
    payload = json.load(__import__("sys").stdin)
    sources = [Source(**item) for item in payload.get("sources", [])]
    print(json.dumps(build_report(sources), indent=2))


if __name__ == "__main__":
    main()
