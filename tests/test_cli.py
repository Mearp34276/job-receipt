import json
from pathlib import Path

from job_receipt.cli import main


def test_cli_report_list_show(tmp_path: Path, capsys):
    store = tmp_path / "store"
    assert main(["--store", str(store), "report", "--operator", "acme", "--job", "job-1"]) == 0
    first = json.loads(capsys.readouterr().out)
    assert main(["--store", str(store), "report", "--operator", "acme", "--job", "job-1"]) == 0
    second = json.loads(capsys.readouterr().out)
    assert first["receipt_id"] == second["receipt_id"]

    assert main(["--store", str(store), "list"]) == 0
    listed = json.loads(capsys.readouterr().out)
    assert len(listed) == 1

    assert main(["--store", str(store), "show", first["receipt_id"]]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["job_id"] == "job-1"

    assert main(["--store", str(store), "show", "rcpt_missing"]) == 1
