# Contributing

Short path for people who clone this repo: set up, run the tests, and open a small pull request.

## Set up a dev environment

Python 3.10 or newer. Continuous integration uses Python 3.12.

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

That is the same install CI uses (`.github/workflows/ci.yml`). The `dev` extra in `pyproject.toml` installs `pytest`, `httpx`, `fastapi`, and `uvicorn`. The package itself has no required runtime dependencies. The optional `online` extra (`pip install -e ".[online]"`) is for running the HTTP API; the test suite already gets those packages from `dev`.

## Run tests

From the repository root, with the virtual environment active:

```bash
python -m pytest
```

`pyproject.toml` sets `pythonpath = ["src"]`. CI runs this same command after `python -m pip install -e ".[dev]"`.

## Report a problem

Use the issue form chooser:

https://github.com/Mearp34276/job-receipt/issues/new/choose

| Form | File | Use it for |
|------|------|------------|
| Bug report | `.github/ISSUE_TEMPLATE/bug_report.yml` | Something broke while installing or running job-receipt |
| Install / usage question | `.github/ISSUE_TEMPLATE/usage_question.yml` | Install or usage questions |
| Commercial quote | `.github/ISSUE_TEMPLATE/commercial.yml` | A quote for install help, priority support, or a custom integration |

Blank issues stay available. Leave secrets, private keys, tokens, and `.env` contents out of issues, logs, and pull requests. Vulnerability reports go through [SECURITY.md](SECURITY.md).

## Pull requests

Keep each pull request small and limited to one change. Say what changed and why.

CI must pass. Pull requests to `master` run the workflow in `.github/workflows/ci.yml`: Python 3.12, `python -m pip install -e ".[dev]"`, then `python -m pytest`.
