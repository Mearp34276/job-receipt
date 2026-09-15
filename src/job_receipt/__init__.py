"""job-receipt — idempotent local receipts for completed jobs."""

from job_receipt.store import Store, Receipt

__all__ = ["Store", "Receipt"]
__version__ = "0.1.0"
