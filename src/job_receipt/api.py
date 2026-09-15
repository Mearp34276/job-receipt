from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from job_receipt import __version__
from job_receipt.store import Receipt, Store

ONLINE_NOTE = "Hosted receipt — no payment, no custody, not a money transmitter."

LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>job-receipt — proof a job finished, exactly once</title>
  <style>
    :root {
      --bg: #0f1419;
      --card: #1a222c;
      --ink: #e8eef4;
      --muted: #93a1b0;
      --line: #2a3644;
      --accent: #7dd3a0;
      --paper: #f4efe6;
      --paper-ink: #1c1916;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
      background: radial-gradient(1200px 600px at 10% -10%, #1c2a22, transparent), var(--bg);
      color: var(--ink);
      line-height: 1.55;
    }
    main { max-width: 760px; margin: 0 auto; padding: 48px 20px 72px; }
    header p { color: var(--muted); margin: 8px 0 0; }
    h1 { font-size: 2rem; letter-spacing: -0.02em; margin: 0; }
    .badge {
      display: inline-block;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.75rem;
      color: var(--accent);
      border: 1px solid #2f5a42;
      border-radius: 999px;
      padding: 2px 10px;
      margin-bottom: 16px;
    }
    .receipt {
      background: var(--paper);
      color: var(--paper-ink);
      border-radius: 6px;
      padding: 22px 24px;
      margin: 28px 0;
      box-shadow: 0 18px 40px rgba(0,0,0,.28);
    }
    .receipt h2 { margin: 0 0 8px; font-size: 1.1rem; }
    .receipt dl { display: grid; grid-template-columns: 8rem 1fr; gap: 6px 12px; margin: 0; }
    .receipt dt { color: #6b6258; }
    .receipt dd { margin: 0; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.92rem; }
    section { margin: 32px 0; }
    h2 { font-size: 1.2rem; }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
    th { color: var(--muted); font-weight: 500; }
    pre, code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    pre {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px 16px;
      overflow-x: auto;
      font-size: 0.85rem;
    }
    a { color: var(--accent); }
    .links a { margin-right: 16px; }
    .fine { color: var(--muted); font-size: 0.92rem; }
    footer { margin-top: 48px; color: var(--muted); font-size: 0.9rem; }
  </style>
</head>
<body>
  <main>
    <div class="badge">ONLINE · hosted receipts</div>
    <header>
      <h1>Proof a job finished — exactly once.</h1>
      <p>Report a completed job. Get an idempotent receipt. Same job again → same receipt. No crypto. No wallets. No payouts.</p>
    </header>

    <div class="receipt">
      <h2>Sample receipt</h2>
      <dl>
        <dt>receipt_id</dt><dd>rcpt_8f3a1c0e2b91d4aa</dd>
        <dt>operator_id</dt><dd>acme</dd>
        <dt>job_id</dt><dd>invoice-sync-2026-09-16</dd>
        <dt>status</dt><dd>recorded</dd>
        <dt>note</dt><dd>Hosted receipt — no payment, no custody.</dd>
      </dl>
    </div>

    <section>
      <h2>Online vs offline</h2>
      <table>
        <tr><th></th><th>Offline CLI</th><th>Online API (this host)</th></tr>
        <tr><td>Where</td><td>Your laptop / CI / cron</td><td>HTTP, shareable across machines</td></tr>
        <tr><td>Store</td><td>Local JSONL</td><td>JSONL on a volume (<code>JOB_RECEIPT_STORE</code>)</td></tr>
        <tr><td>Idempotency</td><td colspan="2"><code>(operator_id, job_id)</code> — same key, same receipt</td></tr>
      </table>
    </section>

    <section>
      <h2>Try it</h2>
      <pre>curl -sS -X POST "$ORIGIN/v1/receipts" \\
  -H "Content-Type: application/json" \\
  -d '{"operator_id":"acme","job_id":"invoice-sync-2026-09-16"}'</pre>
      <p class="fine">If this instance set <code>JOB_RECEIPT_API_KEY</code>, add <code>-H "Authorization: Bearer $JOB_RECEIPT_API_KEY"</code> on <code>/v1</code> routes.</p>
    </section>

    <section class="links">
      <a href="https://github.com/Mearp34276/job-receipt">GitHub</a>
      <a href="/docs">API docs</a>
      <a href="/health">Health</a>
    </section>

    <section>
      <h2>What this is / isn’t</h2>
      <p>A completion ledger with attachable JSON receipts. Not a payment rail, wallet, or money transmitter. Not guaranteed income. Owner: <strong>M.E.</strong></p>
      <p class="fine">Need install help or a custom hook? Open a GitHub Issue with the commercial template. Sponsors is a placeholder until the owner page is approved.</p>
    </section>

    <footer>
      MIT · Owner: M.E. · Technical scaffold only — does not move funds.
    </footer>
  </main>
  <script>
    document.querySelectorAll("pre").forEach(function (el) {
      el.textContent = el.textContent.replaceAll("$ORIGIN", location.origin);
    });
  </script>
</body>
</html>
"""


class ReportBody(BaseModel):
    operator_id: str = Field(..., min_length=1)
    job_id: str = Field(..., min_length=1)


def store_from_env() -> Store:
    raw = os.environ.get("JOB_RECEIPT_STORE")
    return Store(Path(raw) if raw else None)


def api_key_from_env() -> str | None:
    key = os.environ.get("JOB_RECEIPT_API_KEY")
    return key or None


def create_app(store: Store | None = None) -> FastAPI:
    store = store or store_from_env()

    app = FastAPI(
        title="job-receipt",
        description=(
            "Idempotent job completion receipts over HTTP. "
            "Not a payment rail. Not guaranteed income. Owner: M.E."
        ),
        version=__version__,
    )

    def require_api_key(
        authorization: Annotated[str | None, Header()] = None,
    ) -> None:
        expected = api_key_from_env()
        if expected is None:
            return
        if authorization != f"Bearer {expected}":
            raise HTTPException(
                status_code=401,
                detail={"error": "unauthorized"},
            )

    v1 = APIRouter(prefix="/v1", dependencies=[Depends(require_api_key)])

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return LANDING_HTML

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @v1.post("/receipts")
    def report(body: ReportBody) -> dict:
        try:
            receipt = store.report(
                body.operator_id,
                body.job_id,
                note=ONLINE_NOTE,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail={"error": str(exc)}) from exc
        return asdict(receipt)

    @v1.get("/receipts")
    def list_receipts() -> dict[str, list[dict]]:
        return {"receipts": [asdict(r) for r in store.list()]}

    @v1.get("/receipts/{receipt_id}")
    def show_receipt(receipt_id: str) -> dict:
        receipt: Receipt | None = store.get(receipt_id)
        if receipt is None:
            raise HTTPException(
                status_code=404,
                detail={"error": "not_found", "receipt_id": receipt_id},
            )
        return asdict(receipt)

    app.include_router(v1)
    return app


app = create_app()


def serve() -> None:
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("job_receipt.api:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    serve()
