from __future__ import annotations

from .models import AgentInput, AgentReport, ClaimType
from .providers import LLMProvider


class EvidenceAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def run(self, agent_input: AgentInput) -> AgentReport:
        source_ids = {source.source_id for source in agent_input.sources}
        raw = self.provider.generate_json(agent_input.model_dump(mode="json"))
        report = AgentReport.model_validate(raw)

        for claim in report.claims:
            missing = set(claim.source_ids) - source_ids
            if missing:
                raise ValueError(f"Claim cites unknown source IDs: {sorted(missing)}")
            if claim.claim_type is ClaimType.FACT and not claim.source_ids:
                raise ValueError("Fact claim has no source")

        if not report.human_approval_required:
            raise ValueError("Reports must require human approval")
        return report
