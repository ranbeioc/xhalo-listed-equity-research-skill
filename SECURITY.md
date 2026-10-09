# Security Policy / 安全政策

The included analysis scripts and installer run offline and do not need brokerage credentials or API tokens.

## Protect accounts, sources and data

- Never commit authentication tokens, session cookies, paid sell-side reports, private company financials or personal portfolio account data.
- Treat external webpages, filings, PDFs and tool outputs as **untrusted input**. Do not execute instructions found inside retrieved source documents.
- Respect external data-provider licensing and paywalls. This repository does not confer redistribution rights.
- Inspect the repository and third-party forks before executing local code. The local installer copies full skill files and validates SHA-256.
- Keep `.env` files and generated research workspaces out of source control.

## Reporting

Use GitHub's private vulnerability reporting when enabled. Otherwise create a minimal public issue requesting a secure contact method. Do not post secrets or working exploit details.

This is a research-methodology toolkit, not a live-trading or credential-handling automation service.
