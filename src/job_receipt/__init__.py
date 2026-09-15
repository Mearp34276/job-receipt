"""job-receipt — idempotent receipts for completed jobs (offline CLI + optional online API)."""

from job_receipt.store import Store, Receipt

__all__ = ["Store", "Receipt"]
__version__ = "0.2.0"
