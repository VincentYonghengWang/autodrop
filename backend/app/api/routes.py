from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import SessionLocal, get_db
from app.schemas import (
    CheckoutRequest,
    CheckoutResponse,
    DashboardResponse,
    StorefrontResponse,
    TriggerResponse,
    VoiceAssistantRequest,
    VoiceAssistantResponse,
)
from app.services.demo_flow import run_sync_task, simulate_checkout
from app.services.dashboard import get_dashboard_payload
from app.services.storefront import get_storefront_payload
from app.services.voice_assistant import build_voice_reply
from app.worker.tasks import (
    run_listing_pipeline,
    run_ops_loop,
    run_analytics_brain,
    run_douyin_intel,
    run_price_engine,
    run_trend_radar,
)

router = APIRouter()
settings = get_settings()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(db: Session = Depends(get_db)) -> DashboardResponse:
    return get_dashboard_payload(db)


@router.get("/storefront", response_model=StorefrontResponse)
def storefront(db: Session = Depends(get_db)) -> StorefrontResponse:
    return get_storefront_payload(db)


def _trigger_or_run(task_name: str, task) -> TriggerResponse:
    if settings.demo_mode or settings.database_url.startswith("sqlite"):
        with SessionLocal() as db:
            run_sync_task(task_name, db)
            return TriggerResponse(task_name=task_name, status="completed")
    task.delay()
    return TriggerResponse(task_name=task_name, status="queued")


@router.post("/triggers/trend-radar", response_model=TriggerResponse)
def trigger_trend_radar() -> TriggerResponse:
    return _trigger_or_run("trend_radar", run_trend_radar)


@router.post("/triggers/price-engine", response_model=TriggerResponse)
def trigger_price_engine() -> TriggerResponse:
    return _trigger_or_run("price_engine", run_price_engine)


@router.post("/triggers/douyin-intel", response_model=TriggerResponse)
def trigger_douyin_intel() -> TriggerResponse:
    return _trigger_or_run("douyin_intel", run_douyin_intel)


@router.post("/triggers/analytics-brain", response_model=TriggerResponse)
def trigger_analytics_brain() -> TriggerResponse:
    return _trigger_or_run("analytics_brain", run_analytics_brain)


@router.post("/triggers/listing-pipeline", response_model=TriggerResponse)
def trigger_listing_pipeline() -> TriggerResponse:
    return _trigger_or_run("listing_pipeline", run_listing_pipeline)


@router.post("/triggers/ops-loop", response_model=TriggerResponse)
def trigger_ops_loop() -> TriggerResponse:
    return _trigger_or_run("ops_loop", run_ops_loop)


@router.post("/demo/run-all", response_model=TriggerResponse)
def trigger_demo_run_all() -> TriggerResponse:
    if settings.demo_mode or settings.database_url.startswith("sqlite"):
        with SessionLocal() as db:
            run_sync_task("demo_run_all", db)
            return TriggerResponse(task_name="demo_run_all", status="completed")
    return TriggerResponse(task_name="demo_run_all", status="unsupported")


@router.post("/storefront/checkout/{product_id}", response_model=CheckoutResponse)
def checkout_product(product_id: int, payload: CheckoutRequest, db: Session = Depends(get_db)) -> CheckoutResponse:
    try:
        result = simulate_checkout(db, product_id=product_id, email=payload.email)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return CheckoutResponse(**result)


@router.post("/storefront/voice-assistant", response_model=VoiceAssistantResponse)
def storefront_voice_assistant(payload: VoiceAssistantRequest, db: Session = Depends(get_db)) -> VoiceAssistantResponse:
    result = build_voice_reply(payload.question, db)
    return VoiceAssistantResponse(**result)
