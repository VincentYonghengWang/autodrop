from app.core.db import SessionLocal
from app.robots import (
    analytics_brain,
    channel_publisher,
    cs_bot,
    douyin_intel,
    influencer_factory,
    listing_factory,
    order_router,
    price_engine,
    product_scout,
    trend_radar,
)
from app.worker.celery_app import celery_app


@celery_app.task
def run_trend_radar() -> dict:
    with SessionLocal() as db:
        result = trend_radar.run(db)
        product_scout.run(db)
        listing_factory.run(db)
        influencer_factory.run(db)
        return channel_publisher.run(db) | result


@celery_app.task
def run_price_engine() -> dict:
    with SessionLocal() as db:
        return price_engine.run(db)


@celery_app.task
def run_douyin_intel() -> dict:
    with SessionLocal() as db:
        result = douyin_intel.run(db)
        product_scout.run(db)
        return result


@celery_app.task
def run_analytics_brain() -> dict:
    with SessionLocal() as db:
        return analytics_brain.run(db)


@celery_app.task
def run_listing_pipeline() -> dict:
    with SessionLocal() as db:
        listing_factory.run(db)
        influencer_factory.run(db)
        return channel_publisher.run(db)


@celery_app.task
def run_ops_loop() -> dict:
    with SessionLocal() as db:
        order_router.run(db)
        return cs_bot.run(db)
