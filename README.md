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
| `PORT` | `8080` | Listen port (Fly injects this; local default in the image is 8080). |

Writes and reads under `/v1` share the same optional key so a public demo can stay open (leave the var unset) and a private instance can lock the ledger.

### Deploy (Fly.io) — optional, after you deploy

Offline CLI (above) is the primary path and works with no host. Fly.io is optional if you want the HTTP API on a machine you control. Repo includes `Dockerfile` + `fly.toml` (suggested app name `job-receipt`). The Fly account that runs these commands owns the app.

**No public hosted demo is claimed live in this README** until a deploy you run resolves and answers `/health`.

Install [flyctl](https://fly.io/docs/flyctl/install/), then from this repo:

```bash
# Uses the committed fly.toml. --ha=false = one Machine (JSONL is single-writer).
# If "job-receipt" is taken globally, pass another --name.
fly launch --copy-config --no-deploy --ha=false --name job-receipt

# Smallest persistent disk. Skip this and comment out [mounts] in fly.toml
# if you accept an ephemeral store (receipts disappear when the Machine is replaced).
fly volumes create job_receipt_data --size 1

# Optional: lock /v1 routes
fly secrets set JOB_RECEIPT_API_KEY="$(openssl rand -hex 16)"

fly deploy
fly apps open
```

```bash
# Example only — after YOUR deploy succeeds. Replace <your-app> with the name Fly assigned.
curl -sS https://<your-app>.fly.dev/health
curl -sS -X POST https://<your-app>.fly.dev/v1/receipts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JOB_RECEIPT_API_KEY" \
  -d '{"operator_id":"acme","job_id":"invoice-sync-2026-09-16"}'
```

`fly.toml` already points `JOB_RECEIPT_STORE` at `/data/job-receipt` on the volume. Keep `fly scale count 1` — two Machines would not share one JSONL file.

**Honest cost note:** Fly’s public trial is short (not an unlimited forever-free allowance). This config uses the smallest shared VM, `auto_stop_machines = "stop"`, and `min_machines_running = 0` so the Machine sleeps when idle. A 1GB volume is the cheapest persistent disk and can incur a small monthly charge after trial. This repo does not bill anyone and does not move funds.

`render.yaml` / `railway.toml` remain as optional extras. Fly is the suggested host when you choose to deploy — not a live public API in this README.

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

## Also from M.E.

**Related:** [Fort Knox track](https://github.com/Mearp34276/fort-knox-track) — tracks/trains toll plugin, $0.002 USDC on Base, mock by default. Separate free tool. Not required for job-receipt.

Paid install or integration for this repo: [Commercial quote Issue](https://github.com/Mearp34276/job-receipt/issues/new?template=commercial.yml).

## Compliance note

**Technical scaffold — not a money-transmitter license, banking charter, or legal advice. Does not move funds. Do not market as guaranteed income.**

## License

MIT · Owner: M.E.
