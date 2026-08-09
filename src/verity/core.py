"""Deterministic evidence and claim primitives.

The core deliberately does not call an LLM. Model adapters can be layered on top
without changing the provenance model.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Iterable

_SIGNAL = re.compile(
    r"\b(manual|slow|expensive|difficult|frustrat\w*|broken|inefficient|"
    r"spreadsheet|workaround|missing|complain\w*|wish|pain|problem|"
    r"takes?\s+(?:hours?|days?))\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Evidence:
    """A human-approved source fragment."""

    source_id: str
    url: str
    title: str
    text: str


@dataclass(frozen=True)
class Claim:
    """An observation linked directly to its supporting evidence."""

    claim_id: str
    text: str
    kind: str
    source_id: str
    source_url: str
    confidence: float


@dataclass(frozen=True)
class ResearchResult:
    """Serializable result with an explicit review boundary."""

    claims: tuple[Claim, ...]
    hypotheses: tuple[str, ...]
    human_review_required: bool = True

    def to_dict(self) -> dict:
        return {
            "claims": [asdict(c) for c in self.claims],
            "hypotheses": list(self.hypotheses),
            "human_review_required": self.human_review_required,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


def _claim_id(source_id: str, text: str) -> str:
    digest = hashlib.sha256(f"{source_id}\n{text}".encode("utf-8")).hexdigest()
    return f"clm_{digest[:16]}"


def _sentences(text: str) -> Iterable[str]:
    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        sentence = sentence.strip()
        if sentence:
            yield sentence


def build_claims(evidence: Iterable[Evidence]) -> ResearchResult:
    """Extract explicit research signals while retaining source provenance."""

    claims: list[Claim] = []
    for item in evidence:
        for sentence in _sentences(item.text):
            if not _SIGNAL.search(sentence):
                continue
            claims.append(
                Claim(
                    claim_id=_claim_id(item.source_id, sentence),
                    text=sentence,
                    kind="observation",
                    source_id=item.source_id,
                    source_url=item.url,
                    confidence=0.5,
                )
            )

    hypotheses = tuple(
        f"Repeated observation may indicate an opportunity: {claim.text}"
        for claim in claims
    )
    return ResearchResult(tuple(claims), hypotheses)
