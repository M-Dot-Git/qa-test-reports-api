from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_service_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "qa-test-reports-api",
        "status": "ready",
    }


def test_gateway_health_endpoint_returns_service_status() -> None:
    response = client.get("/api/test-reports/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "qa-test-reports-api",
        "status": "ready",
    }


def test_summary_endpoint_returns_coherent_generated_report_data() -> None:
    for path in ("/summary", "/api/test-reports/summary"):
        response = client.get(path)

        assert response.status_code == 200
        payload = response.json()
        totals = payload["totals"]
        trend = payload["trend"]
        suites = payload["suites"]

        assert payload["generated_at"]
        assert len(trend) == 7
        assert len(suites) == 4
        assert len({point["date"] for point in trend}) == 7
        assert totals["executed"] == totals["passed"] + totals["failed"] + totals["skipped"]
        assert totals["passed"] == sum(point["passed"] for point in trend)
        assert totals["failed"] == sum(point["failed"] for point in trend)
        assert totals["skipped"] == sum(point["skipped"] for point in trend)
        assert totals["passed"] == sum(suite["passed"] for suite in suites)
        assert totals["failed"] == sum(suite["failed"] for suite in suites)
        assert totals["skipped"] == sum(suite["skipped"] for suite in suites)
        assert totals["pass_rate"] == round(
            totals["passed"] / totals["executed"] * 100,
            1,
        )
        assert all(
            isinstance(value, int) and value >= 0
            for group in [totals, *trend, *suites]
            for key, value in group.items()
            if key in {"passed", "failed", "skipped", "executed"}
        )
