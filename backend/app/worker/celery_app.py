from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery("autodrop", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "trend-radar-30m": {"task": "app.worker.tasks.run_trend_radar", "schedule": 60 * 30},
        "price-engine-4h": {"task": "app.worker.tasks.run_price_engine", "schedule": 60 * 60 * 4},
        "douyin-intel-2h": {"task": "app.worker.tasks.run_douyin_intel", "schedule": 60 * 60 * 2},
        "analytics-brain-daily": {"task": "app.worker.tasks.run_analytics_brain", "schedule": 60 * 60 * 24},
        "listing-factory-hourly": {"task": "app.worker.tasks.run_listing_pipeline", "schedule": 60 * 60},
        "ops-loop-hourly": {"task": "app.worker.tasks.run_ops_loop", "schedule": 60 * 60},
    },
)

celery_app.autodiscover_tasks(["app.worker"])

