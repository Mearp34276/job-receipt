# Launch posts (drafts — not posted)

**Owner:** M.E.

Paste-ready copy for one Show HN and one short Reddit / Indie Hackers-style post. **Nothing here is published** until M.E. pastes it. This file is not a launch announcement and not evidence of traffic, signups, or revenue.

## Honesty (do not soften when pasting)

- **No income guarantees.** Free MIT use is the product. A commercial quote is optional paid work a buyer requests. It is not a promise that anyone earns money.
- **Sponsors is not live.** `https://github.com/sponsors/Mearp34276` is a placeholder until GitHub approves Sponsors on the owner account. Do not say the project is receiving sponsor money.
- **No live public demo.** Checked 2026-09-23: `https://job-receipt.fly.dev` does not resolve. Do not claim that host is up. README Fly curls are examples for **after** someone deploys their own app.
- **No metrics.** Do not add stars, users, revenue, or “$100/day” to these posts.

Repo: https://github.com/Mearp34276/job-receipt

Commercial quote Issue (template `commercial.yml`, label `commercial`):  
https://github.com/Mearp34276/job-receipt/issues/new?template=commercial.yml

## Show HN

**Title**

```
Show HN: Job Receipt – idempotent proof a job finished, offline, no database
```

**URL**

```
https://github.com/Mearp34276/job-receipt
```

**Text**

```
Job Receipt is a small MIT tool that records “this job finished” as an idempotent receipt.

Same operator + job id returns the same receipt. Reporting again does not double-count. The default path is an offline CLI and a local JSONL file: no signup, no database, no SaaS account.

Logs are a weak attachment when a client, ticket, or invoice asks whether the work finished. They rotate, they get grepped differently, and retries add lines. A receipt is a stable id you can attach.

An optional HTTP API in the same repo uses the same receipt rules if you later want CI, a laptop, and a worker to share one store. You deploy that yourself. This post does not claim a live public demo. https://job-receipt.fly.dev is not up.

What it is not: a wallet, a payment rail, crypto, or guaranteed income. Free MIT use needs nothing else.

Owner: M.E.
Repo: https://github.com/Mearp34276/job-receipt

Paid install help, priority support, or a one-off integration is optional. Open a Commercial quote Issue (free use does not require this):
https://github.com/Mearp34276/job-receipt/issues/new?template=commercial.yml

Install/help quotes are often $150–$500 after you describe the job. That is a range for work someone asks for, not a guarantee that anyone earns it.

GitHub Sponsors for Mearp34276 is not live until GitHub approves the account. This project is not receiving sponsor money.
```

## Reddit / Indie Hackers (one short post)

Use this as a single post (Side Project, Indie Hackers, or similar). Do not post it twice as if they were different launches.

**Title**

```
Offline idempotent job receipts (MIT) — proof a job finished without a database
```

**Text**

```
job-receipt is a free MIT CLI that writes an idempotent completion receipt for a job.

Why not logs: a log line is not a stable id. Retries, rotation, and “did the cron actually finish?” make logs a weak attachment for a client, ticket, or invoice. Report (operator, job) once, get a receipt id. Report again, get the same receipt. The store is a local JSONL file. It works offline. No signup.

An optional HTTP API is in the repo if you want to self-host later. There is no live public demo. https://job-receipt.fly.dev is not up. README Fly curls are examples for after you deploy your own app.

Owner: M.E.
License: MIT
Repo: https://github.com/Mearp34276/job-receipt

Paid install / support quote (optional; free use stays free):
https://github.com/Mearp34276/job-receipt/issues/new?template=commercial.yml

No income guarantees. GitHub Sponsors on Mearp34276 is not live until GitHub approves it. This post is not a claim that the project is earning money.
```
