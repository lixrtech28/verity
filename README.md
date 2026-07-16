# Opportunity Intelligence Agent

A local-first learning project and monetizable service engine. It converts a **human-approved research packet** into:

- source-backed facts;
- clearly labeled inferences and unknowns;
- a workflow hypothesis;
- discovery questions;
- a respectful outreach draft;
- an explicit human-approval record.

It deliberately does **not** scrape restricted websites, send messages, or make consequential decisions autonomously.

## Why this agent

The fastest zero-capital agent business is usually an agent-powered service. This project supports a service such as:

> I research target accounts, map their likely workflow, identify evidence-backed triggers, and prepare human-reviewed discovery outreach.

The customer pays for accurate preparation and qualified conversations, not for the agent itself.

## Architecture

```text
Human-curated public sources
          ↓
Pydantic input validation
          ↓
Replaceable provider adapter
(mock / OpenAI / Anthropic / Ollama)
          ↓
Structured evidence report
          ↓
Invariant checks
          ↓
Human review and approval
```

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
pytest -q
opportunity-agent run examples/company_packet.json
```

The default `mock` provider costs nothing and proves the complete pipeline.

## Frontier and local providers

```bash
# OpenAI
export OPENAI_API_KEY="..."
opportunity-agent run examples/company_packet.json --provider openai --model YOUR_MODEL

# Anthropic
export ANTHROPIC_API_KEY="..."
opportunity-agent run examples/company_packet.json --provider anthropic --model YOUR_MODEL

# Local open-weight model through Ollama
ollama pull qwen3:8b
ollama serve
opportunity-agent run examples/company_packet.json --provider ollama --model qwen3:8b
```

Model names change. Pass a model currently available in your account or local runtime.

## First paid workflow

1. Select one niche and buyer.
2. Use client-approved public sources or client-provided materials.
3. Run the packet through the agent.
4. Verify every factual claim.
5. Deliver account briefs, workflow hypotheses, and discovery questions.
6. Charge for a bounded pilot.
7. Store corrections as evaluation cases.
8. Automate only safe repeated steps.

## Security boundaries

- Never commit credentials or customer data.
- Do not expose local Ollama or development services to the public internet.
- Do not let model output execute commands or modify external systems without allowlists and approval.
- Treat web pages, documents, and tool output as untrusted input.
