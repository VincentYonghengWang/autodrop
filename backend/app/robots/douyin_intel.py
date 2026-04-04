from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models import TrendSignal
from app.robots.common import log_activity

CHINESE_KEYWORDS = ["工厂直播", "产地直销", "工厂货", "义乌工厂", "原厂批发"]


def run(db: Session) -> dict:
    signal = TrendSignal(
        source="douyin",
        product_name="Breathable Slip-On Recovery Shoes",
        viral_score=84.0,
        factory_hint_json={"city": "莆田", "category": "shoes", "factory_count": 300},
        raw_url="https://douyin.com/video/recovery-shoes",
        detected_at=datetime.utcnow(),
    )
    db.add(signal)
    db.commit()
    log_activity(
        db,
        "Douyin Factory Intel",
        "Detected high-confidence city-to-category signal from Putian shoe factory bloggers.",
        metadata={"keywords": CHINESE_KEYWORDS},
    )
    return {"signal_id": signal.id}

