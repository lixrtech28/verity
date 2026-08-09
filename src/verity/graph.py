"""Small, deterministic evidence graph primitives.

The graph stores relationships between claims. It does not decide whether a
relationship is true; callers must provide the relationship and its rationale.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from typing import Iterable


@dataclass(frozen=True)
class Relation:
    source: str
    target: str
    relation: str
    rationale: str = ""


class EvidenceGraph:
    """Directed graph for support, contradiction, and derivation links."""

    ALLOWED = frozenset({"supports", "contradicts", "derived_from", "related_to"})

    def __init__(self, relations: Iterable[Relation] = ()) -> None:
        self._relations: list[Relation] = []
        for relation in relations:
            self.add(relation)

    def add(self, relation: Relation) -> None:
        if relation.relation not in self.ALLOWED:
            raise ValueError(f"unsupported relation: {relation.relation}")
        if not relation.source or not relation.target:
            raise ValueError("source and target are required")
        if relation.source == relation.target:
            raise ValueError("self-relations are not allowed")
        if relation not in self._relations:
            self._relations.append(relation)

    @property
    def relations(self) -> tuple[Relation, ...]:
        return tuple(self._relations)

    def neighbors(self, node_id: str, relation: str | None = None) -> tuple[str, ...]:
        return tuple(
            r.target
            for r in self._relations
            if r.source == node_id and (relation is None or r.relation == relation)
        )

    def contradictions(self) -> tuple[Relation, ...]:
        return tuple(r for r in self._relations if r.relation == "contradicts")

    def to_dict(self) -> dict:
        return {"relations": [asdict(r) for r in self._relations]}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
