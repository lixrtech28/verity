# Agent Engineering Rules

- Preserve the evidence boundary: facts require source IDs.
- Never add automatic email sending, social-platform automation, or unrestricted web scraping.
- All consequential external actions require explicit human approval.
- Keep providers replaceable behind `LLMProvider`.
- Add tests for every safety invariant and bug fix.
- Prefer one complete vertical workflow over many incomplete features.
- Never commit credentials or customer data.
