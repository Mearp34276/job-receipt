# job-receipt

**Proof a job finished — exactly once — without a database, SaaS, or wallet.**

Offline CLI for scripts, cron, CI, and agents. Report a completed job → get an **idempotent receipt**. Same job again → same receipt. No crypto. No network. No custody.

**Owner:** M.E.

## Why use this tomorrow

You already run jobs. Clients, tickets, and invoices ask: *did it finish?* Logs lie. Spreadsheets drift. Retries double-count.

| You need | job-receipt gives you |
|----------|------------------------|
| Proof for a client / ticket / invoice | Attachable JSON receipt |
| Safe retries | Idempotent on `(operator, job)` |
| Something that works offline today | Local files only — no signup |
| A path to get paid for the work around it | Free tool → **paid support / install** when someone’s stuck |

**Who:** freelancers, ops, indie hackers, agent builders who need **billable completion proof** without Postgres or Stripe.

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## Use

```bash
# Record completion (safe to retry)
job-receipt report --operator acme --job invoice-sync-2026-09-16

job-receipt list
job-receipt show <receipt_id>
```

Store defaults to `./.job-receipt/` (local files only).

### Wrap a script

```bash
#!/usr/bin/env bash
set -euo pipefail
# ... do the real work ...
job-receipt report --operator "$USER" --job "backup-$(date -u +%F)"
```

## Earn path (honest)

**Go-live ≠ guaranteed dollars tomorrow.** Publishing opens a door; money comes from real buyers.

| When | What |
|------|------|
| **Now (free)** | Use / fork / star — MIT forever for personal and most use |
| **Commercial** | Open a GitHub Issue with label **`commercial`** (or the Commercial quote template) for priority support, custom install, or a one-off integration |
| **Sponsors** | Placeholder: https://github.com/sponsors/Mearp34276 — **enable Sponsors on the owner account; link goes live after GitHub approves** |
| **Later** | Optional hosted inbox — not in this MVP |

### Commercial pricing (honest ranges)

| Offer | Typical range |
|-------|---------------|
| Install / setup help | **$150–$500** |
| Priority support | Quoted |
| Larger integrations | Quoted after scope |

Details: [docs/COMMERCIAL.md](docs/COMMERCIAL.md). These are estimates for paid work buyers request — **not** income guarantees.

We never claim “install this → $100/day.” Revenue = support, custom work, or hosted extras people ask for.

## Sponsors

If you want to support maintenance without a custom project:

- Link (goes live after GitHub approves Sponsors on the owner account): https://github.com/sponsors/Mearp34276
- Owner enable steps: [docs/SPONSORS.md](docs/SPONSORS.md)

Sponsors is **not claimed live** until that page shows a real sponsorship profile.

## What this is / isn’t

| Is | Isn’t |
|----|--------|
| Local completion ledger + receipt | A payment rail or wallet |
| Free open-source utility | Guaranteed income |
| Proof-of-completion for jobs you run | Fort Knox / live USDC tolls |

## Compliance note

**Technical scaffold — not a money-transmitter license, banking charter, or legal advice. Does not move funds. Do not market as guaranteed income.**

## License

MIT · Owner: M.E.
