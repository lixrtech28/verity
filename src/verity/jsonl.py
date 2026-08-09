"""JSONL helpers for batch and streaming research pipelines."""

from __future__ import annotations

import json
from typing import Iterable, Iterator

from .core import Evidence


def evidence_from_jsonl(lines: Iterable[str]) -> Iterator[Evidence]:
    """Yield Evidence records from newline-delimited JSON."""
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            yield Evidence(
                source_id=str(item["source_id"]),
                url=str(item["url"]),
                title=str(item["title"]),
                text=str(item["text"]),
            )
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ValueError(f"invalid evidence JSONL at line {number}") from exc


def evidence_to_jsonl(items: Iterable[Evidence]) -> str:
    """Serialize evidence records deterministically as JSONL."""
    return "\n".join(
        json.dumps(item.__dict__, ensure_ascii=False, sort_keys=True)
        for item in items
    )
