from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from job_receipt.store import Store


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="job-receipt",
        description="Report a completed job once; get an idempotent local receipt.",
    )
    parser.add_argument(
        "--store",
        type=Path,
        default=None,
        help="Store directory (default: ./.job-receipt)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_report = sub.add_parser("report", help="Record a completed job (idempotent)")
    p_report.add_argument("--operator", required=True)
    p_report.add_argument("--job", required=True)

    sub.add_parser("list", help="List receipts")

    p_show = sub.add_parser("show", help="Show one receipt by id")
    p_show.add_argument("receipt_id")

    args = parser.parse_args(argv)
    store = Store(args.store)

    if args.cmd == "report":
        r = store.report(args.operator, args.job)
        print(json.dumps(asdict(r), indent=2))
        return 0
    if args.cmd == "list":
        print(json.dumps([asdict(r) for r in store.list()], indent=2))
        return 0
    if args.cmd == "show":
        r = store.get(args.receipt_id)
        if not r:
            print(json.dumps({"error": "not_found", "receipt_id": args.receipt_id}))
            return 1
        print(json.dumps(asdict(r), indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
