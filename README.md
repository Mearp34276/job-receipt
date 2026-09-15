# job-receipt

**Proof a job finished — exactly once — without a database, SaaS, or wallet.**

Report a completed job → get an **idempotent receipt**. Same job again → same receipt. No crypto. No custody. No payouts.

Use it **offline** (CLI, local JSONL) or **online** (hosted HTTP API, same receipts).

**Owner:** M.E.

## Why use this tomorrow

You already run jobs. Clients, tickets, and invoices ask: *did it finish?* Logs lie. Spreadsheets drift. Retries double-count.

| You need | job-receipt gives you |
|----------|------------------------|
| Proof for a client / ticket / invoice | Attachable JSON receipt |
| Safe retries | Idempotent on `(operator, job)` |
| Something that works offline today | Local files only — no signup |
| The same proof over the network | Hosted HTTP API (optional extra) |
| A path to get paid for the work around it | Free tool → **paid support / install** when someone’s stuck |

**Who:** freelancers, ops, indie hackers, agent builders who need **billable completion proof** without Postgres or Stripe.

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Offline CLI is the default. For the hosted API:

```bash
pip install -e ".[online]"
```

## Use (offline CLI)

```bash
# Record completion (safe to retry)
job-receipt report --operator acme --job invoice-sync-2026-09-16

job-receipt list
job-receipt show <receipt_id>
```

Store defaults to `./.job-receipt/` (local files only), or `$JOB_RECEIPT_STORE` if set.

### Wrap a script

```bash
#!/usr/bin/env bash
set -euo pipefail
# ... do the real work ...
job-receipt report --operator "$USER" --job "backup-$(date -u +%F)"
```

## Online (hosted HTTP API)

**Why online:** the CLI is for one machine. The API is for operators who need the same idempotent receipt from CI, a laptop, and a worker box — one store, over HTTP.

**Why still use offline:** no process to run, no port, no key. Scripts and cron stay local.

Same product rules either way: idempotent on `(operator_id, job_id)`, MIT, no wallets, no fund movement.

### Run locally

```bash
pip install -e ".[online]"
uvicorn job_receipt.api:app --host 0.0.0.0 --port 8000
# or: python -m job_receipt.api
```

Open `/` for the product page. OpenAPI lives at `/docs`.

### curl

```bash
# Health (always public)
curl -sS http://127.0.0.1:8000/health

# Record (idempotent). Repeat → same receipt_id
curl -sS -X POST http://127.0.0.1:8000/v1/receipts \
  -H "Content-Type: application/json" \
  -d '{"operator_id":"acme","job_id":"invoice-sync-2026-09-16"}'

curl -sS http://127.0.0.1:8000/v1/receipts
curl -sS http://127.0.0.1:8000/v1/receipts/<receipt_id>
```

### Environment

| Variable | Default | Role |
|----------|---------|------|
| `JOB_RECEIPT_STORE` | `./.job-receipt` (cwd) | Directory for `receipts.jsonl`. Point this at a mounted volume on PaaS. |
| `JOB_RECEIPT_API_KEY` | unset | If set, every `/v1/*` request needs `Authorization: Bearer <key>`. `/` and `/health` stay public. |
| `PORT` | `8000` | Listen port (Render / Railway inject this). |

Writes and reads under `/v1` share the same optional key so a public demo can stay open (leave the var unset) and a private instance can lock the ledger.

### Deploy (free-tier path)

Repo includes `Dockerfile`, `render.yaml`, and `railway.toml`.

**Render (preferred free web service):**

1. Push this repo to GitHub.
2. [Render Dashboard](https://dashboard.render.com) → New → Blueprint, or New Web Service from the repo.
3. `render.yaml` selects Docker + free plan + `/health`.
4. Set `JOB_RECEIPT_STORE=/var/data/job-receipt`.
5. Optional: set `JOB_RECEIPT_API_KEY` in the dashboard (`sync: false` in the Blueprint).
6. Free disks are ephemeral across deploys. For a store that survives, attach a persistent disk at `/var/data` (paid on Render) and keep the same env var.

**Railway:**

1. New project → deploy from repo (Dockerfile is detected; `railway.toml` sets `/health`).
2. Set `JOB_RECEIPT_STORE=/var/data/job-receipt`.
3. Optional: add a volume mounted at `/var/data`, and optional `JOB_RECEIPT_API_KEY`.

```bash
# After deploy
curl -sS https://YOUR-HOST/health
curl -sS -X POST https://YOUR-HOST/v1/receipts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JOB_RECEIPT_API_KEY" \
  -d '{"operator_id":"acme","job_id":"invoice-sync-2026-09-16"}'
```

No Stripe, no billing, no multi-tenant SaaS in this tree.

## Earn path (honest)

**Go-live ≠ guaranteed dollars tomorrow.** Publishing opens a door; money comes from real buyers.

| When | What |
|------|------|
| **Now (free)** | Use / fork / star — MIT forever for personal and most use |
| **Commercial** | Open a GitHub Issue with label **`commercial`** (or the Commercial quote template) for priority support, custom install, or a one-off integration |
| **Sponsors** | Placeholder: https://github.com/sponsors/Mearp34276 — **enable Sponsors on the owner account; link goes live after GitHub approves** |
| **Hosted** | Online API in this repo — still receipts only, not a paid inbox or payment rail |

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
| Completion ledger + receipt (CLI or HTTP) | A payment rail or wallet |
| Free open-source utility | Guaranteed income |
| Proof-of-completion for jobs you run | Fort Knox / live USDC tolls |

## Compliance note

**Technical scaffold — not a money-transmitter license, banking charter, or legal advice. Does not move funds. Do not market as guaranteed income.**

## License

MIT · Owner: M.E.
