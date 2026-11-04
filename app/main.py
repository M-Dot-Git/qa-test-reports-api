from datetime import date, datetime, timedelta, timezone
from random import randint

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="QA Test Reports API")

SUITE_NAMES = ("API", "Web UI", "Mobile", "Regression")
RESULT_TYPES = ("passed", "failed", "skipped")


class ResultCounts(BaseModel):
    passed: int
    failed: int
    skipped: int


class ReportTotals(ResultCounts):
    executed: int
    pass_rate: float


class TrendPoint(ResultCounts):
    date: date


class SuiteSummary(ResultCounts):
    name: str


class ReportSummary(BaseModel):
    generated_at: datetime
    totals: ReportTotals
    trend: list[TrendPoint]
    suites: list[SuiteSummary]


@app.get("/health")
@app.get("/api/test-reports/health")
async def health() -> dict[str, str]:
    return {"service": "qa-test-reports-api", "status": "ready"}


@app.get("/summary", response_model=ReportSummary)
@app.get("/api/test-reports/summary", response_model=ReportSummary)
async def report_summary() -> ReportSummary:
    generated_at = datetime.now(timezone.utc)
    suite_counts = {
        name: {result_type: 0 for result_type in RESULT_TYPES}
        for name in SUITE_NAMES
    }
    trend: list[TrendPoint] = []

    for days_ago in reversed(range(7)):
        daily_counts = {result_type: 0 for result_type in RESULT_TYPES}
        for suite_name in SUITE_NAMES:
            results = {
                "passed": randint(25, 90),
                "failed": randint(0, 12),
                "skipped": randint(0, 4),
            }
            for result_type, count in results.items():
                suite_counts[suite_name][result_type] += count
                daily_counts[result_type] += count

        trend.append(
            TrendPoint(
                date=generated_at.date() - timedelta(days=days_ago),
                **daily_counts,
            )
        )

    totals = {
        result_type: sum(counts[result_type] for counts in suite_counts.values())
        for result_type in RESULT_TYPES
    }
    executed = sum(totals.values())
    return ReportSummary(
        generated_at=generated_at,
        totals=ReportTotals(
            **totals,
            executed=executed,
            pass_rate=round(totals["passed"] / executed * 100, 1),
        ),
        trend=trend,
        suites=[
            SuiteSummary(name=name, **counts)
            for name, counts in suite_counts.items()
        ],
    )
