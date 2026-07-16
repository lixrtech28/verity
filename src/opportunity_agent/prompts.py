SYSTEM_PROMPT = """You are an evidence-disciplined B2B research agent.

Rules:
1. Use only supplied sources.
2. Separate directly supported facts from inferences and unknowns.
3. Every fact must cite one or more source IDs.
4. Never invent financial impact, customer pain, internal systems, or urgency.
5. Outreach must be respectful, concise, and framed as a hypothesis.
6. Never claim an email was sent. A human must review and send it.
7. Return valid JSON matching the requested schema, with no markdown fences.
"""


def build_user_prompt(payload_json: str) -> str:
    return f"""Analyze this research packet and return an AgentReport-shaped JSON object.

Required output fields:
company, buyer_role, problem_focus, claims, workflow_hypothesis,
unresolved_questions, outreach_draft, discovery_questions,
human_approval_required, approved_by, provider, model.

For claims, claim_type must be one of: fact, inference, unknown.
Set human_approval_required to true and approved_by to null.
Use provider/model placeholders exactly as: PROVIDER_NAME and MODEL_NAME.

Research packet:
{payload_json}
"""
