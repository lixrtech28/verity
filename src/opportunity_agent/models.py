from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ClaimType(str, Enum):
    FACT = "fact"
    INFERENCE = "inference"
    UNKNOWN = "unknown"


class Source(BaseModel):
    source_id: str
    title: str
    url: HttpUrl | None = None
    text: str = Field(min_length=1)
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Claim(BaseModel):
    text: str
    claim_type: ClaimType
    source_ids: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)

    @field_validator("source_ids")
    @classmethod
    def facts_need_sources(cls, value: list[str], info):
        if info.data.get("claim_type") == ClaimType.FACT and not value:
            raise ValueError("Facts require at least one source_id")
        return value


class AgentInput(BaseModel):
    company: str
    buyer_role: str
    problem_focus: str
    sources: list[Source]


class AgentReport(BaseModel):
    company: str
    buyer_role: str
    problem_focus: str
    claims: list[Claim]
    workflow_hypothesis: list[str]
    unresolved_questions: list[str]
    outreach_draft: str
    discovery_questions: list[str]
    human_approval_required: bool = True
    approved_by: str | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provider: str
    model: str

    def save_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.model_dump_json(indent=2), encoding="utf-8")
