# Banking Use Case

A PySpark data pipeline that deduplicates transactions and filters out
records with null amounts, deployed to Databricks as a scheduled job via
Databricks Asset Bundles, with CI/CD on GitHub Actions.

## Project structure

```
.
├── src/
│   ├── transformations.py   # dedup_transactions, filter_null_amounts
│   └── main.py               # job entry point (reads/writes tables)
├── tests/
│   └── test_transformations.py
├── conftest.py                # shared pytest `spark` fixture
├── resources/
│   └── banking_use_case.job.yml   # Databricks job definition (schedule, task)
├── databricks.yml             # Databricks Asset Bundle config (dev/prod targets)
├── run_tests.ps1              # one-shot local test runner (Windows)
└── .github/workflows/
    ├── tests.yml               # runs pytest on every push/PR
    └── deploy.yml               # tests + deploys the bundle to Databricks on push to main
```

## Transformations

- `dedup_transactions(df, subset=None)` — drops duplicate rows, optionally
  keyed on a subset of columns (e.g. `transaction_id`).
- `filter_null_amounts(df, amount_col="amount")` — drops rows where the
  amount column is null.

`src/main.py` chains both and writes the result to a target table.

## Running tests locally

Requires Python 3.12+ and a JDK (PySpark needs Java 17+).

```powershell
.\run_tests.ps1
```

This script sets `JAVA_HOME` and `PYSPARK_PYTHON` (both required for PySpark
to work on Windows) and runs `pytest tests/ -v` using the project's `.venv`.

First-time setup, if `.venv` doesn't exist yet:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install pyspark pytest
```

## CI/CD

**`tests.yml`** — runs on every push and pull request. Installs Python,
Java 17, and `pyspark`/`pytest`, then runs the test suite. This is the gate:
if tests fail, nothing deploys.

**`deploy.yml`** — runs on push to `main`. Runs the same test suite, then
installs the Databricks CLI and runs `databricks bundle deploy -t prod` to
push the job definition to the Databricks workspace.

Deploy requires two repository secrets (Settings → Secrets and variables →
Actions):

| Secret | Value |
|---|---|
| `DATABRICKS_HOST` | Workspace URL, e.g. `https://dbc-xxxxxxxx-xxxx.cloud.databricks.com` |
| `DATABRICKS_TOKEN` | A personal access token with `all-apis` scope (see note below) |

## Databricks job

Deploying the bundle creates/updates a job named
`banking-transformations-${bundle.target}` with a single task
(`run_transformations`) that runs `src/main.py` on **serverless compute**.
It's scheduled to run **daily at 06:00 UTC** (`resources/banking_use_case.job.yml`).

`src/main.py` currently points at placeholder table names:

```python
SOURCE_TABLE = "banking_use_case.transactions"
TARGET_TABLE = "banking_use_case.transactions_clean"
```

Update these to real catalog.schema.table names before relying on the
scheduled run — until then, the daily run will fail because the source
table doesn't exist.

## Notes on this workspace (Databricks Free Edition)

- Only **serverless compute** is supported — job tasks must use
  `environment_key` (declared under `environments:`), not `new_cluster`.
- Personal access tokens must be generated with the **`all-apis`** scope.
  A token scoped only to e.g. `sql` will fail bundle deploys with
  `403: Provided access token does not have required scopes: workspace`.
- The `prod` target in `databricks.yml` sets an explicit
  `workspace.root_path` — Databricks requires this for any target with
  `mode: production`.
