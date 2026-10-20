# Security

## Report a vulnerability

Report a vulnerability privately with GitHub private vulnerability reporting (Security Advisories) for this repository:

https://github.com/Mearp34276/job-receipt/security/advisories/new

On the repository **Security** tab, choose **Report a vulnerability**. The report stays in a private security advisory. Include what you can about impact and how to reproduce it, with secrets removed.

If the **Report a vulnerability** button is not shown, private reporting is not enabled yet. In that case, open a public issue titled `Security contact request` with no technical details, and the maintainer will reply with a private channel.

This repository has no security email address. Public issues are for bugs and usage questions ([CONTRIBUTING.md](CONTRIBUTING.md)).

## Supported versions

| Version | Supported |
|---------|-----------|
| [v0.1.0](https://github.com/Mearp34276/job-receipt/releases/tag/v0.1.0) | Yes |
| `master` | Yes |

The package version in `pyproject.toml` is `0.2.0`. Fixes for supported versions land on `master`.

## Receipts only

job-receipt records an idempotent completion receipt. It does not move funds, hold a wallet, or send payments. There is no live-send switch.

The offline CLI writes a local JSONL file. The store directory is `$JOB_RECEIPT_STORE`, or `./.job-receipt` when that variable is unset. The optional HTTP API serves the same receipts. If `JOB_RECEIPT_API_KEY` is set, every `/v1/*` request needs `Authorization: Bearer <key>`. `/` and `/health` stay public. When the variable is unset, `/v1` on that instance is open.

Do not commit API keys, tokens, or `.env` contents, and leave them out of issues and pull requests.
