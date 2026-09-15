from pathlib import Path

from job_receipt.store import Store


def test_report_is_idempotent(tmp_path: Path):
    store = Store(tmp_path)
    a = store.report("op-1", "job-9")
    b = store.report("op-1", "job-9")
    assert a.receipt_id == b.receipt_id
    assert a.job_id == "job-9"
    assert a.status == "recorded"


def test_different_jobs_get_different_receipts(tmp_path: Path):
    store = Store(tmp_path)
    a = store.report("op-1", "job-a")
    b = store.report("op-1", "job-b")
    assert a.receipt_id != b.receipt_id
    assert len(store.list()) == 2
