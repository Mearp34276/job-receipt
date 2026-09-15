# Why job-receipt (positioning)

## One-liner
Idempotent proof that a job completed — offline CLI today, optional hosted HTTP API — with zero crypto and zero payouts.

## Differentiator
Not another logger. Not a wallet. Not a SaaS meter.
It’s a **receipt**: report once, get a stable id, retry-safe, attachable to tickets/invoices.

Offline is local JSONL. Online is the same store over HTTP (`JOB_RECEIPT_STORE` on a volume). Pick one per deploy; the receipt contract does not change.
