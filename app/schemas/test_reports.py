from datetime import date, datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    service: str
    status: str


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
