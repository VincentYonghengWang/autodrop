from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas import DashboardResponse, TriggerResponse
from app.services.dashboard import get_dashboard_payload
from app.worker.tasks import (
    run_analytics_brain,
    run_douyin_intel,
    run_price_engine,
    run_trend_radar,
)

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(db: Session = Depends(get_db)) -> DashboardResponse:
    return get_dashboard_payload(db)


@router.post("/triggers/trend-radar", response_model=TriggerResponse)
def trigger_trend_radar() -> TriggerResponse:
    run_trend_radar.delay()
    return TriggerResponse(task_name="trend_radar", status="queued")


@router.post("/triggers/price-engine", response_model=TriggerResponse)
def trigger_price_engine() -> TriggerResponse:
    run_price_engine.delay()
    return TriggerResponse(task_name="price_engine", status="queued")


@router.post("/triggers/douyin-intel", response_model=TriggerResponse)
def trigger_douyin_intel() -> TriggerResponse:
    run_douyin_intel.delay()
    return TriggerResponse(task_name="douyin_intel", status="queued")


@router.post("/triggers/analytics-brain", response_model=TriggerResponse)
def trigger_analytics_brain() -> TriggerResponse:
    run_analytics_brain.delay()
    return TriggerResponse(task_name="analytics_brain", status="queued")

