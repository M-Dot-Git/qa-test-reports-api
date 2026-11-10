# QA Test Reports API

Standalone FastAPI microservice for test-report functionality. It is reachable
on the internal Compose network; clients should call it through `qa-insights-api`,
which validates the Keycloak bearer token and proxies `/api/test-reports/*`.

The health endpoint is `/health`. `GET /api/test-reports/summary` returns a
fresh randomized seven-day snapshot with totals, daily results, and per-suite
results. The dashboard renders the snapshot as Chart.js visualizations.

HTTP routes are in `app/api/routes/`, response models in `app/schemas/`,
summary assembly in `app/services/`, and generated sample results in
`app/dummy_data/`. This service currently has no database layer; report
repositories and persistence models should be added when storage requirements
are defined.

Run locally with:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Run tests with `pytest -q`.

IGNORE: This line is added in this repo to create a pr request and review in ui.
