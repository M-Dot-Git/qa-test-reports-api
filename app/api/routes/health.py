from fastapi import APIRouter

from ...schemas.test_reports import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(service="qa-test-reports-api", status="ready")
