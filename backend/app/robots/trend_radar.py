from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import TrendSignal
from app.robots.common import log_activity

settings = get_settings()

TREND_QUERIES = {
    "tiktok": ["#tiktokmademebuyit", "#amazonfinds", "#productreview"],
    "instagram": ["#amazonfinds", "#musthave", "#productreview", "#unboxing"],
    "douyin": ["工厂", "产地", "直播", "义乌", "莆田", "深圳华强北", "汕头", "东莞", "佛山"],
    "amazon": ["Movers and Shakers"],
    "google": ["shopping rising queries"],
}

CURATED_SIGNAL_QUEUE = [
    {
        "source": "instagram",
        "product_name": "Portable Blender Bottle Matte Black",
        "viral_score": 74.0,
        "raw_url": "https://instagram.com/reel/blender-bottle-matte-black",
    },
    {
        "source": "tiktok",
        "product_name": "Breathable Slip-On Recovery Shoes Slate",
        "viral_score": 78.0,
        "factory_hint_json": {"city": "莆田", "category": "shoes", "factory_count": 260},
        "raw_url": "https://tiktok.com/@nova/video/recovery-shoes-slate",
    },
    {
        "source": "amazon",
        "product_name": "Sunset Projection Lamp Aurora Edition",
        "viral_score": 72.0,
        "raw_url": "https://amazon.com/dp/sunset-lamp-aurora",
    },
    {
        "source": "instagram",
        "product_name": "Car Seat Gap Organizer Leather Trim",
        "viral_score": 70.0,
        "raw_url": "https://instagram.com/reel/car-gap-organizer-leather",
    },
    {
        "source": "douyin",
        "product_name": "Magnetic Cable Organizer Walnut Desk Set",
        "viral_score": 76.0,
        "factory_hint_json": {"city": "义乌", "category": "small_goods", "factory_count": 220},
        "raw_url": "https://douyin.com/video/cable-organizer-walnut",
    },
    {
        "source": "tiktok",
        "product_name": "Foldable Walking Pad Quiet Edition",
        "viral_score": 75.0,
        "raw_url": "https://tiktok.com/@vida/video/walking-pad-quiet",
    },
]


def run(db: Session) -> dict:
    existing_names = set(db.scalars(select(TrendSignal.product_name)).all())
    next_signal = next((signal for signal in CURATED_SIGNAL_QUEUE if signal["product_name"] not in existing_names), None)
    if not next_signal:
        log_activity(
            db,
            "Trend Radar",
            "All curated trend slots are already live. The current product lineup remains active until the queue is refreshed.",
            metadata={"queries": TREND_QUERIES, "queue_size": len(CURATED_SIGNAL_QUEUE)},
        )
        return {"inserted": 0, "sources": list(TREND_QUERIES), "skipped": True}

    if next_signal["viral_score"] < settings.viral_score_threshold:
        log_activity(
            db,
            "Trend Radar",
            f"{next_signal['product_name']} did not clear the viral score threshold.",
            status="warning",
            metadata={"queries": TREND_QUERIES, "product_name": next_signal["product_name"]},
        )
        return {"inserted": 0, "sources": list(TREND_QUERIES), "skipped": True}

    db.add(TrendSignal(**next_signal, detected_at=datetime.utcnow()))
    db.commit()
    log_activity(
        db,
        "Trend Radar",
        f"Queued {next_signal['product_name']} from {next_signal['source'].title()} and pushed it into the product pipeline.",
        metadata={"queries": TREND_QUERIES, "product_name": next_signal["product_name"]},
    )
    return {"inserted": 1, "sources": list(TREND_QUERIES), "skipped": False, "product_name": next_signal["product_name"]}
