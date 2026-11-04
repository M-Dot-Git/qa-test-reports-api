from fastapi import APIRouter

from ...schemas.test_reports import ReportSummary
from ...services.test_reports import get_report_summary

router = APIRouter(prefix="/api/test-reports", tags=["Test reports"])


@router.get("/summary", response_model=ReportSummary)
async def report_summary() -> ReportSummary:
    return get_report_summary()
