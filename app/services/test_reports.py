from datetime import datetime, timezone

from ..dummy_data.test_reports import SUITE_NAMES, generate_daily_results
from ..schemas.test_reports import (
    ReportSummary,
    ReportTotals,
    SuiteSummary,
    TrendPoint,
)

RESULT_TYPES = ("passed", "failed", "skipped")


def get_report_summary() -> ReportSummary:
    generated_at = datetime.now(timezone.utc)
    suite_counts = {
        name: {result_type: 0 for result_type in RESULT_TYPES}
        for name in SUITE_NAMES
    }
    trend: list[TrendPoint] = []

    for point in generate_daily_results(generated_at.date()):
        daily_counts = {result_type: 0 for result_type in RESULT_TYPES}
        for suite_name, results in point["suites"].items():
            for result_type, count in results.items():
                suite_counts[suite_name][result_type] += count
                daily_counts[result_type] += count
        trend.append(TrendPoint(date=point["date"], **daily_counts))

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
