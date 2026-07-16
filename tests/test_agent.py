import json
from pathlib import Path

import pytest

from opportunity_agent.agent import EvidenceAgent
from opportunity_agent.models import AgentInput
from opportunity_agent.providers import MockProvider


def load_example() -> AgentInput:
    payload = json.loads(Path("examples/company_packet.json").read_text())
    return AgentInput.model_validate(payload)


def test_mock_agent_produces_cited_facts():
    report = EvidenceAgent(MockProvider()).run(load_example())
    assert report.human_approval_required is True
    assert report.claims
    assert all(claim.source_ids for claim in report.claims)
    assert report.provider == "mock"


def test_unknown_source_id_is_rejected():
    class BadProvider(MockProvider):
        def generate_json(self, payload):
            output = super().generate_json(payload)
            output["claims"][0]["source_ids"] = ["DOES_NOT_EXIST"]
            return output

    with pytest.raises(ValueError, match="unknown source IDs"):
        EvidenceAgent(BadProvider()).run(load_example())
