from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from uuid import uuid4


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    operator_id: str
    job_id: str
    status: str
    created_at: str
    note: str = "Local receipt only — no payment, no custody, no network call."


class Store:
    """Append-only JSONL store. Idempotent on (operator_id, job_id)."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or (Path.cwd() / ".job-receipt")
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "receipts.jsonl"
        self._lock = Lock()
        self._by_key: dict[tuple[str, str], Receipt] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.is_file():
            return
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            data = json.loads(line)
            r = Receipt(**data)
            self._by_key[(r.operator_id, r.job_id)] = r

    def report(self, operator_id: str, job_id: str) -> Receipt:
        if not operator_id or not job_id:
            raise ValueError("operator_id and job_id are required")
        key = (operator_id, job_id)
        with self._lock:
            existing = self._by_key.get(key)
            if existing:
                return existing
            receipt = Receipt(
                receipt_id=f"rcpt_{uuid4().hex[:16]}",
                operator_id=operator_id,
                job_id=job_id,
                status="recorded",
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(asdict(receipt)) + "\n")
            self._by_key[key] = receipt
            return receipt

    def list(self) -> list[Receipt]:
        with self._lock:
            return list(self._by_key.values())

    def get(self, receipt_id: str) -> Receipt | None:
        with self._lock:
            for r in self._by_key.values():
                if r.receipt_id == receipt_id:
                    return r
        return None
