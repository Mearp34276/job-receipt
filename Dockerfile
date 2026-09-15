FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ".[online]" \
    && mkdir -p /data/job-receipt

ENV JOB_RECEIPT_STORE=/data/job-receipt
ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "uvicorn job_receipt.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
