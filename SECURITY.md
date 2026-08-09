# Security Policy

## Scope

Security reports for this project are welcome, especially issues involving unsafe handling of untrusted research sources, prompt injection, data leakage, or unintended external actions.

## Reporting

Please do not publish sensitive vulnerability details in a public issue before maintainers have had an opportunity to assess them. Open a private GitHub security advisory when available, or contact the maintainer through the contact method listed on the repository profile.

## Design principles

- Treat retrieved content as untrusted input.
- Keep credentials outside model-visible data.
- Require explicit approval before external side effects.
- Preserve provenance for generated findings.
