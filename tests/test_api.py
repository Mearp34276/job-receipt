from pathlib import Path

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from job_receipt.api import create_app
from job_receipt.store import Store


def client_for(tmp_path: Path) -> TestClient:
    return TestClient(create_app(Store(tmp_path)))


def test_health(tmp_path: Path):
    r = client_for(tmp_path).get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_landing_is_html(tmp_path: Path):
    r = client_for(tmp_path).get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "job-receipt" in r.text
    assert "https://github.com/Mearp34276/job-receipt" in r.text
    assert "M.E." in r.text
    assert "not a money transmitter" in r.text.lower() or "does not move funds" in r.text.lower()


def test_report_is_idempotent(tmp_path: Path):
    client = client_for(tmp_path)
    body = {"operator_id": "op-1", "job_id": "job-9"}
    a = client.post("/v1/receipts", json=body)
    b = client.post("/v1/receipts", json=body)
    assert a.status_code == 200
    assert b.status_code == 200
    assert a.json()["receipt_id"] == b.json()["receipt_id"]
    assert a.json()["job_id"] == "job-9"
    assert a.json()["status"] == "recorded"
    listed = client.get("/v1/receipts")
    assert listed.status_code == 200
    assert len(listed.json()["receipts"]) == 1


def test_show_and_missing(tmp_path: Path):
    client = client_for(tmp_path)
    created = client.post(
        "/v1/receipts",
        json={"operator_id": "op-1", "job_id": "job-a"},
    ).json()
    shown = client.get(f"/v1/receipts/{created['receipt_id']}")
    assert shown.status_code == 200
    assert shown.json()["receipt_id"] == created["receipt_id"]
    missing = client.get("/v1/receipts/rcpt_does_not_exist")
    assert missing.status_code == 404


def test_api_key_guards_v1_when_set(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("JOB_RECEIPT_API_KEY", "secret-test-key")
    client = client_for(tmp_path)
    body = {"operator_id": "op-1", "job_id": "job-9"}
    denied = client.post("/v1/receipts", json=body)
    assert denied.status_code == 401
    allowed = client.post(
        "/v1/receipts",
        json=body,
        headers={"Authorization": "Bearer secret-test-key"},
    )
    assert allowed.status_code == 200
    listed = client.get("/v1/receipts")
    assert listed.status_code == 401
    listed_ok = client.get(
        "/v1/receipts",
        headers={"Authorization": "Bearer secret-test-key"},
    )
    assert listed_ok.status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/").status_code == 200
