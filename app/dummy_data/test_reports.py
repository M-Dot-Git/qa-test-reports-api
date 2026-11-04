from datetime import date, timedelta
from random import randint
from typing import TypedDict

SUITE_NAMES = ("API", "Web UI", "Mobile", "Regression")


class DailyResults(TypedDict):
    date: date
    suites: dict[str, dict[str, int]]


def generate_daily_results(end_date: date) -> list[DailyResults]:
    results: list[DailyResults] = []
    for days_ago in reversed(range(7)):
        suites = {
            suite_name: {
                "passed": randint(25, 90),
                "failed": randint(0, 12),
                "skipped": randint(0, 4),
            }
            for suite_name in SUITE_NAMES
        }
        results.append(
            {
                "date": end_date - timedelta(days=days_ago),
                "suites": suites,
            }
        )
    return results
