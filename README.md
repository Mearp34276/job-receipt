# job-receipt

**Proof a job finished — exactly once — without a database, SaaS, or wallet.**

Offline CLI for scripts, cron, CI, and agents. Report a completed job → get an **idempotent receipt**. Same job again → same receipt. No crypto. No network. No custody.

**Owner:** M.E.

## Why this exists (reason to use it)

Most “did it run?” answers are messy logs, screenshots, or a spreadsheet someone forgets to update. Retries double-count. Dashboards need accounts.

`job-receipt` is different:

| Pain | What job-receipt does |
|------|------------------------|
| “Did this cron/agent job already succeed?” | Idempotent on `(operator, job)` — safe to retry |
| “I need proof for a client / ticket / invoice” | Machine-readable JSON receipt you can attach |
| “I don’t want another cloud meter or wallet” | 100% local — airgap / laptop / CI runner friendly |
| “I need this today, not after onboarding” | `pip install` → report → done |

**Who it’s for:** freelancers, ops folks, indie hackers, and agent builders who need a **billable or auditable completion proof** without standing up Postgres or Stripe.

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Or from this repo after clone:

```bash
cd job-receipt
pip install -e ".[dev]"
```

## Use

```bash
# Record completion (safe to retry)
job-receipt report --operator acme --job invoice-sync-2026-09-16

# List / inspect
job-receipt list
job-receipt show <receipt_id>
```

Store defaults to `./.job-receipt/` (local files only).

### Example: wrap a script

```bash
#!/usr/bin/env bash
set -euo pipefail
# ... do the real work ...
job-receipt report --operator "$USER" --job "backup-$(date -u +%F)"
```

## What this is / isn’t

| Is | Isn’t |
|----|--------|
| Local completion ledger + receipt | A payment rail or wallet |
| Free open-source utility | A guarantee of income |
| Proof-of-completion for jobs you already run | Fort Knox / live USDC tolls |

## Commercial / support

Open-source (MIT) is free forever for personal and most use.

**Paid options (when you’re ready to earn from it):**

1. **Priority support / custom install** — open an Issue with label `commercial` or email via GitHub profile  
2. **GitHub Sponsors** — once enabled on the owner account (link will live here)  
3. **Hosted inbox (later)** — optional SaaS meter; not in this MVP  

We never claim “install this → $100/day.” Revenue comes from real buyers of support, licenses, or hosted extras.

## Compliance note

**Technical scaffold — not a money-transmitter license, banking charter, or legal advice. Does not move funds. Do not market as guaranteed income.**

## License

MIT · Owner: M.E.
