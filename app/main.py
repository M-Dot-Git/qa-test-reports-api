from fastapi import FastAPI

from .api.routes import health, test_reports

app = FastAPI(title="QA Test Reports API")
app.include_router(health.router)
app.include_router(test_reports.router)
