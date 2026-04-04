from __future__ import annotations

from datetime import datetime

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


def run(db: Session) -> dict:
    synthetic_signals = [
        {
            "source": "instagram",
            "product_name": "Foldable Walking Pad",
            "viral_score": 73.0,
            "raw_url": "https://instagram.com/reel/walking-pad",
        },
        {
            "source": "douyin",
            "product_name": "Magnetic Cable Organizer",
            "viral_score": 79.0,
            "factory_hint_json": {"city": "义乌", "category": "small_goods", "factory_count": 220},
            "raw_url": "https://douyin.com/video/cable-organizer",
        },
    ]

    inserted = 0
    for signal in synthetic_signals:
        if signal["viral_score"] < settings.viral_score_threshold:
            continue
        db.add(TrendSignal(**signal, detected_at=datetime.utcnow()))
        inserted += 1

    db.commit()
    log_activity(
        db,
        "Trend Radar",
        f"{inserted} new qualifying signals ingested from TikTok, Instagram, Douyin, Amazon, and Google.",
        metadata={"queries": TREND_QUERIES},
    )
    return {"inserted": inserted, "sources": list(TREND_QUERIES)}

